import random
import time

import allure
import requests

from config import SW_OAP_URL, SW_AUTH_TOKEN


class SkyWalking:
    """SkyWalking 链路查询库（纯封装 OAP GraphQL，不侵入测试框架）。

    用法示例:
        from Common.skywalking import SkyWalking
        sw = SkyWalking()

        # 1. 按 traceId 精确查链路（打印 + 挂 Allure）
        sw.locate("04dd56512ea04a7aa57ab280f81d7f14.158.17866887361121923")

        # 2. 按 服务/接口/时间窗 查最近链路（名字自动解析成 ID）
        traces = sw.search_traces(service_name="fht-dist",
                                  start=sw.minutes_ago(60), end=sw.now_minute())

        # 3. 按请求时刻反查链路（自己记录 t0 毫秒时间戳）
        trace_id = sw.locate_latest(endpoint="POST:/dist/commission/settle",
                                    t0=1786688736112)
        if trace_id:
            sw.locate(trace_id)

        # 4. 查某条 trace 的后端日志（技术型失败定位用）
        logs = sw.query_logs(trace_id=trace_id, keyword="Exception")

        # 5. 元数据
        services = sw.get_services()
        endpoints = sw.search_endpoints("commission")

        # 6. 时间窗工具
        sw.now_minute()            # "2026-08-14 1030"
        sw.minutes_ago(15)         # 15 分钟前
    """

    def __init__(self, oap_url: str = None, auth_token: str = None, timeout: int = 10):
        self.oap_url = (oap_url or SW_OAP_URL).rstrip("/")
        self.auth_token = auth_token if auth_token is not None else SW_AUTH_TOKEN
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = False

    # ===================================================================
    # OAP GraphQL 基础
    # ===================================================================
    def _gql(self, query: str, variables: dict = None):
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authentication"] = self.auth_token
        resp = self.session.post(
            f"{self.oap_url}/graphql",
            json={"query": query, "variables": variables or {}},
            headers=headers,
            timeout=self.timeout,
        )
        assert resp.status_code == 200, f"OAP 请求失败 HTTP {resp.status_code}: {resp.text[:500]}"
        data = resp.json()
        if "errors" in data:
            raise RuntimeError(f"OAP GraphQL 错误: {data['errors']}")
        return data["data"]

    # ===================================================================
    # 元数据
    # ===================================================================
    def get_services(self, start: str = None, end: str = None, group: str = None):
        """查询服务列表（默认近 24 小时内有上报的服务）。"""
        start = start or self.minutes_ago(1440)
        end = end or self.now_minute()
        query = """
        query($duration: Duration!, $group: String) {
          getAllServices(duration: $duration, group: $group) { id name group shortName normal }
        }
        """
        data = self._gql(query, {"duration": {"start": start, "end": end, "step": "MINUTE"},
                                 "group": group})
        return data.get("getAllServices") or []

    def search_endpoints(self, keyword: str, service_id: str = None, limit: int = 10):
        """按关键字搜索接口（返回 [{id, name}]）。service_id 缺省时遍历所有服务。"""
        query = """
        query($keyword: String!, $serviceId: ID!, $limit: Int!) {
          searchEndpoint(keyword: $keyword, serviceId: $serviceId, limit: $limit) { id name }
        }
        """
        if service_id:
            data = self._gql(query, {"keyword": keyword, "serviceId": service_id, "limit": limit})
            return data.get("searchEndpoint") or []
        merged = {}
        for s in self.get_services():
            data = self._gql(query, {"keyword": keyword, "serviceId": s["id"], "limit": limit})
            for ep in data.get("searchEndpoint") or []:
                merged[ep["id"]] = ep
        return list(merged.values())[:limit]

    def _resolve_service_id(self, name: str) -> str:
        for s in self.get_services():
            if s["name"] == name:
                return s["id"]
        return None

    def _resolve_endpoint_id(self, name: str, service_id: str = None) -> str:
        for ep in self.search_endpoints(name, service_id=service_id, limit=200):
            ep_path = ep["name"].split(":", 1)[-1]
            if ep_path == name or ep["name"] == name:
                return ep["id"]
        return None

    # ===================================================================
    # 查链路
    # ===================================================================
    def query_trace(self, trace_id: str):
        """按 traceId 查询完整链路，返回 span 列表（未查到返回空列表）。"""
        query = """
        query($traceId: ID!) {
          queryTrace(traceId: $traceId) {
            spans {
              traceId segmentId spanId parentSpanId serviceCode serviceInstanceName
              startTime endTime endpointName type peer component isError layer
              tags { key value }
              logs { time data { key value } }
            }
          }
        }
        """
        data = self._gql(query, {"traceId": trace_id})
        trace = data.get("queryTrace")
        if not trace or not trace.get("spans"):
            return []
        return trace["spans"]

    def query_basic_traces(self, service: str = None, endpoint: str = None, trace_id: str = None,
                           start: str = None, end: str = None,
                           page: int = 1, page_size: int = 10,
                           query_order: str = "BY_DURATION"):
        """按条件查最近链路（service/endpoint 传 OAP ID，名字自动解析请用 search_traces）。

        :param service: 服务 ID（如 get_services 返回的 id）
        :param endpoint: 接口 ID（如 search_endpoints 返回的 id）
        :param trace_id: 精确 traceId
        :param query_order: BY_DURATION=按耗时降序 / BY_START_TIME=按时间倒序（后者利于查最新）
        """
        start = start or self.minutes_ago(60)
        end = end or self.now_minute()
        query = """
        query($condition: TraceQueryCondition!) {
          queryBasicTraces(condition: $condition) {
            traces { segmentId endpointNames start duration isError traceIds }
          }
        }
        """
        condition = {
            "queryDuration": {"start": start, "end": end, "step": "MINUTE"},
            "traceState": "ALL",
            "queryOrder": query_order,
            "paging": {"pageNum": page, "pageSize": page_size},
        }
        if service:
            condition["serviceId"] = service
        if endpoint:
            condition["endpointId"] = endpoint
        if trace_id:
            condition["traceId"] = trace_id
        data = self._gql(query, {"condition": condition})
        return (data.get("queryBasicTraces") or {}).get("traces") or []

    def search_traces(self, service_name: str = None, endpoint_name: str = None,
                      start: str = None, end: str = None, page: int = 1, page_size: int = 10):
        """按 服务名/接口名 + 时间窗 查最近链路（名字自动解析成 OAP ID）。

        示例:
            sw.search_traces(service_name="fht-dist",
                             endpoint_name="POST:/dist/commission/settle",
                             start=sw.minutes_ago(30), end=sw.now_minute())
        """
        service_id = self._resolve_service_id(service_name) if service_name else None
        if not service_id and service_name:
            raise ValueError(f"未找到服务: {service_name}")
        endpoint_id = self._resolve_endpoint_id(endpoint_name, service_id) if endpoint_name else None
        if not endpoint_id and endpoint_name:
            raise ValueError(f"未找到接口: {endpoint_name}")
        return self.query_basic_traces(service=service_id, endpoint=endpoint_id,
                                       start=start, end=end, page=page, page_size=page_size)

    # ===================================================================
    # 查日志
    # ===================================================================
    def query_logs(self, trace_id: str = None, service: str = None, keyword: str = None,
                   start: str = None, end: str = None, page: int = 1, page_size: int = 20):
        """按 traceId / 服务 / 关键字 + 时间窗 查后端日志。

        :param trace_id: traceId，精确关联某条链路
        :param service: 服务名（自动解析）
        :param keyword: 内容关键字（如 Exception / ERROR）
        """
        start = start or self.minutes_ago(60)
        end = end or self.now_minute()
        query = """
        query($condition: LogQueryCondition!) {
          queryLogs(condition: $condition) {
            logs {
              serviceName serviceInstanceName traceId timestamp content
              tags { key value }
            }
            errorReason
          }
        }
        """
        condition = {
            "queryDuration": {"start": start, "end": end, "step": "MINUTE"},
            "queryOrder": "DES",
            "paging": {"pageNum": page, "pageSize": page_size},
        }
        if trace_id:
            condition["relatedTrace"] = {"traceId": trace_id}
        if service:
            service_id = self._resolve_service_id(service)
            if service_id:
                condition["serviceId"] = service_id
        if keyword:
            condition["keywordsOfContent"] = [keyword]
        data = self._gql(query, {"condition": condition})
        return (data.get("queryLogs") or {}).get("logs") or []

    # ===================================================================
    # 格式化 / 输出
    # ===================================================================
    def build_chain(self, spans):
        """按 段内 parentSpanId / 各段入口 组装调用链，返回 [(depth, span), ...]"""
        if not spans:
            return []
        children_map = {}
        for s in spans:
            children_map.setdefault((s["segmentId"], s.get("parentSpanId")), []).append(s)
        roots = [s for s in spans if s.get("parentSpanId") in (-1, None)]
        roots.sort(key=lambda s: s.get("startTime") or 0)
        chain = []

        def walk(span, depth):
            chain.append((depth, span))
            for c in sorted(
                children_map.get((span["segmentId"], span["spanId"]), []),
                key=lambda x: x.get("startTime") or 0,
            ):
                walk(c, depth + 1)

        for r in roots:
            walk(r, 0)
        if not chain:
            chain = [(0, s) for s in sorted(spans, key=lambda s: s.get("startTime") or 0)]
        return chain

    @staticmethod
    def _service_chain(spans) -> str:
        seen = []
        for s in sorted(spans, key=lambda s: s.get("startTime") or 0):
            if s.get("parentSpanId") in (-1, None):
                sc = s.get("serviceCode")
                if not seen or seen[-1] != sc:
                    seen.append(sc)
        return " → ".join(seen) if seen else "-"

    @staticmethod
    def _ms(start, end) -> str:
        if start and end:
            return f"{int((end - start) / 1000)}ms"
        return ""

    def format_trace(self, trace_id: str, spans: list = None) -> str:
        """格式化链路摘要（markdown 文本）。"""
        spans = spans if spans is not None else self.query_trace(trace_id)
        if not spans:
            return f"未查询到 trace `{trace_id}`"
        lines = [f"## SkyWalking Trace `{trace_id}`", f"\n服务链: {self._service_chain(spans)}", ""]
        lines.append("### 调用链")
        for depth, s in self.build_chain(spans):
            flag = " ⚠ERROR" if s.get("isError") else ""
            lines.append(
                f"{'  ' * depth}- [{s.get('serviceCode')}] {s.get('endpointName')} "
                f"({self._ms(s.get('startTime'), s.get('endTime'))}){flag} "
                f"peer={s.get('peer') or '-'} component={s.get('component') or '-'}"
            )
        db_stmts = [
            t["value"]
            for s in spans
            for t in (s.get("tags") or [])
            if t.get("key") in ("db.statement", "db.bind_variables") and t.get("value")
        ]
        if db_stmts:
            lines += ["", "### DB 语句"]
            for st in db_stmts[:20]:
                lines.append(f"- `{st[:300]}`")
        errors = [s for s in spans if s.get("isError")]
        if errors:
            lines += ["", "### 错误详情"]
            for s in errors:
                lines.append(f"- **{s.get('serviceCode')}** `{s.get('endpointName')}`")
                for lg in s.get("logs") or []:
                    for kv in lg.get("data") or []:
                        if kv.get("key") in ("stack", "error", "message") and kv.get("value"):
                            lines.append(f"  - {kv['key']}: {kv['value'][:1500]}")
        return "\n".join(lines)

    def save_to_allure(self, trace_id: str, spans: list = None):
        """把链路摘要写入 Allure 报告。"""
        text = self.format_trace(trace_id, spans)
        allure.attach(text, name=f"SkyWalking Trace {trace_id}",
                      attachment_type=allure.attachment_type.TEXT)

    def locate(self, trace_id: str):
        """一键定位：打印链路摘要 + 挂 Allure。异常不外抛。"""
        try:
            spans = self.query_trace(trace_id)
            text = self.format_trace(trace_id, spans)
            print(f"\n===== SkyWalking Trace {trace_id} =====")
            print(text)
            try:
                self.save_to_allure(trace_id, spans)
            except Exception as e:
                print(f"[skywalking] allure 挂载失败: {e}")
            return text
        except Exception as e:
            print(f"[skywalking] 定位失败: {e}")
            return None

    def _match_trace(self, traces, endpoint_id, endpoint, t0, threshold_ms):
        if not traces:
            return None
        if endpoint_id is None and endpoint:
            key = endpoint.split(":", 1)[-1].split("?", 1)[0]
            traces = [t for t in traces if key in " ".join(t.get("endpointNames") or [])]
        if not traces:
            return None
        traces.sort(key=lambda t: abs(int(t["start"]) - t0))
        best = traces[0]
        if abs(int(best["start"]) - t0) > threshold_ms:
            return None
        return (best.get("traceIds") or [None])[0]

    def locate_latest(self, endpoint: str = None, service_name: str = None, t0: int = None,
                      window_min: int = 30, threshold_ms: int = 30000,
                      retry: int = 5, retry_interval: int = 2) -> str:
        """按 时间窗 + 接口最近匹配反查 trace（网关不透传传播头时用）。

        OAP 的 BasicTrace 索引对窄时间窗有延迟（约 20-30s 才可见），
        因此默认用宽窗口 + 按时间倒序，刚请求完即可命中。

        :param endpoint: 形如 GET:/system/auth/get-permission-info（可只传路径，自动解析成 OAP 接口 ID）
        :param service_name: 服务名（可选，加速接口 ID 解析）
        :param t0: 请求发出前的本地时间戳（毫秒）；不传取当前
        :param window_min: 向前查询的时间窗口（分钟）
        :param threshold_ms: 与 t0 的最大时间差，超过视为未命中
        :param retry: 查询为空时的重试次数（兜底，通常不需要）
        :param retry_interval: 每次重试间隔秒数
        :return: 匹配的 trace_id；未命中返回 None
        """
        t0 = t0 or int(time.time() * 1000)
        start = time.strftime("%Y-%m-%d %H%M", time.localtime((t0 - window_min * 60 * 1000) / 1000))
        end = time.strftime("%Y-%m-%d %H%M", time.localtime((t0 + 60000) / 1000))
        service_id = self._resolve_service_id(service_name) if service_name else None
        endpoint_id = None
        if endpoint:
            ep_name = endpoint.split(":", 1)[-1].split("?", 1)[0]
            endpoint_id = self._resolve_endpoint_id(ep_name, service_id)
        for attempt in range(retry + 1):
            traces = self.query_basic_traces(service=service_id, endpoint=endpoint_id,
                                             start=start, end=end, page_size=200,
                                             query_order="BY_START_TIME")
            trace_id = self._match_trace(traces, endpoint_id, endpoint, t0, threshold_ms)
            if trace_id:
                return trace_id
            if attempt < retry:
                time.sleep(retry_interval)
        return None

    # ===================================================================
    # 时间窗工具
    # ===================================================================
    @staticmethod
    def now_minute() -> str:
        """当前时间，格式 YYYY-MM-DD HHmm（OAP Duration 用）。"""
        return time.strftime("%Y-%m-%d %H%M")

    @staticmethod
    def minutes_ago(n: int) -> str:
        """n 分钟前的时间，格式 YYYY-MM-DD HHmm。"""
        return time.strftime("%Y-%m-%d %H%M", time.localtime(time.time() - n * 60))
