"""
Grafana Loki 日志查询模块

功能:
  - 查询指定服务的日志
  - 按运单号过滤日志
  - 查询错误日志
  - 支持自定义 LogQL 表达式

使用示例:
    from Common.grafana_loki import fetch_waybill_logs, fetch_service_logs, fetch_error_logs
    import time

    now_ms = int(time.time() * 1000)
    one_hour_ago_ms = now_ms - 3600 * 1000

    # 查询运单号日志
    logs = fetch_waybill_logs("SF1225198841659", one_hour_ago_ms, now_ms)

    # 查询服务日志
    logs = fetch_service_logs("fht-recycle", one_hour_ago_ms, now_ms)

    # 查询错误日志
    error_logs = fetch_error_logs("fht-recycle", one_hour_ago_ms, now_ms)

    # 输出 JSON
    import json
    print(json.dumps(logs, ensure_ascii=False, indent=2))
"""
import os
import json
import requests
from datetime import datetime

# ============================================================
# 配置
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAFANA_FILE = os.path.join(PROJECT_ROOT, "Date", "Grafana.yaml")

# Loki 数据源配置
LOKI_DATASOURCE_UID = "P8E80F9AEF21F6940"
LOKI_DATASOURCE_ID = 3

# 服务名与 LogQL 映射
SERVICE_MAP = {
    "fht-recycle": {"app": "fht-recycle", "job": "prod-yhs/fht-recycle"},
    "fht-dist": {"app": "fht-dist", "job": "prod-yhs/fht-dist"},
    "fht-member": {"app": "fht-member", "job": "prod-yhs/fht-member"},
    "fht-pay": {"app": "fht-pay", "job": "prod-yhs/fht-pay"},
    "fht-trade": {"app": "fht-trade", "job": "prod-yhs/fht-trade"},
    "fht-system": {"app": "fht-system", "job": "prod-yhs/fht-system"},
}


# ============================================================
# 配置加载（复用现有逻辑）
# ============================================================
def load_grafana_config():
    """从 Date/Grafana.yaml 读取 Grafana 连接信息（行格式：URL / user / password）"""
    with open(GRAFANA_FILE, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if len(lines) < 3:
        raise RuntimeError(f"Grafana.yaml 格式异常，需 3 行: URL/user/password")
    # 提取 base URL（去掉路径和查询参数）
    url = lines[0].split("/dashboard")[0].split("/d/")[0].rstrip("/")
    return url, lines[1], lines[2]


def grafana_session():
    """创建带 Basic Auth 的 Grafana session"""
    url, user, pwd = load_grafana_config()
    s = requests.Session()
    s.verify = False
    s.auth = (user, pwd)
    s.headers.update({"Content-Type": "application/json"})
    return url, s


# ============================================================
# 工具函数
# ============================================================
def _ms_to_datetime(ms):
    """毫秒时间戳转可读时间"""
    return datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def _datetime_to_ms(dt_str):
    """可读时间转毫秒时间戳 (格式: '2026-08-28 10:30:15')"""
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp() * 1000)


# ============================================================
# 核心查询方法
# ============================================================
def grafana_loki_fetch(url, gs, logql, from_ms, to_ms, max_lines=1000, direction="backward"):
    """
    调用 Grafana Loki 查询日志

    参数:
        url: Grafana base URL
        gs: requests.Session (带 Basic Auth)
        logql: LogQL 查询表达式
            - 全量: '{app="fht-recycle"}'
            - 关键词过滤: '{app="fht-recycle"} |= `SF1225198841659`'
            - 正则过滤: '{job="prod-yhs/fht-recycle"} |~ "(?i)(error|exception)"'
        from_ms: 开始时间戳(毫秒)
        to_ms: 结束时间戳(毫秒)
        max_lines: 返回日志行数上限 (默认1000)
        direction: 查询方向 "backward"=最新在前, "forward"=最旧在前

    返回:
        [
            {
                "timestamp": "2026-08-28 10:30:15.123",
                "timestamp_ms": 1787902215123,
                "line": "原始日志内容",
                "labels": {"app": "fht-recycle", ...}
            },
            ...
        ]
    """
    payload = {
        "from": str(int(from_ms)),
        "to": str(int(to_ms)),
        "queries": [{
            "refId": "A",
            "expr": logql,
            "queryType": "range",
            "datasource": {"type": "loki", "uid": LOKI_DATASOURCE_UID},
            "editorMode": "builder",
            "direction": direction,
            "maxLines": max_lines,
            "step": "",
            "legendFormat": "",
            "datasourceId": LOKI_DATASOURCE_ID,
            "intervalMs": 200,
            "maxDataPoints": 1252,
        }],
    }

    try:
        r = gs.post(
            f"{url}/api/ds/query",
            params={"ds_type": "loki", "requestId": "explore_auto"},
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"  ❌ Loki 请求失败: {e}")
        return []

    # 解析响应
    results = r.json().get("results", {}).get("A", {})
    if results.get("error"):
        print(f"  ❌ Loki 查询错误: {results['error']}")
        return []

    frames = results.get("frames", [])
    logs = []

    for frame in frames:
        data = frame.get("data", {})
        values = data.get("values", [])

        # Loki 响应结构:
        #   values[0] = labels (dict array)
        #   values[1] = timestamps (milliseconds)
        #   values[2] = log lines (string array)
        #   values[3] = nanosecond timestamps (string array)
        #   values[4] = label types (dict array)
        #   values[5] = id (string array)
        if len(values) < 3:
            continue

        labels_list = values[0] if values[0] else []
        timestamps = values[1] if values[1] else []
        lines = values[2] if values[2] else []

        for i, line in enumerate(lines):
            if line is None:
                continue

            ts = timestamps[i] if i < len(timestamps) else 0
            labels = labels_list[i] if i < len(labels_list) else {}

            logs.append({
                "timestamp": _ms_to_datetime(ts),
                "timestamp_ms": ts,
                "line": line,
                "labels": labels,
            })

    return logs


# ============================================================
# 便捷查询方法
# ============================================================
def fetch_service_logs(service, from_ms, to_ms, limit=1000):
    """
    查询指定服务的日志

    参数:
        service: 服务名 (如 "fht-recycle", "fht-dist", "fht-member")
        from_ms: 开始时间戳(毫秒)
        to_ms: 结束时间戳(毫秒)
        limit: 返回行数上限

    返回: 日志列表
    """
    url, gs = grafana_session()

    # 构造 LogQL
    if service in SERVICE_MAP:
        logql = f'{{app="{SERVICE_MAP[service]["app"]}"}}'
    else:
        logql = f'{{app="{service}"}}'

    return grafana_loki_fetch(url, gs, logql, from_ms, to_ms, max_lines=limit)


def fetch_waybill_logs(waybill_no, from_ms, to_ms, limit=1000):
    """
    按运单号查询日志

    参数:
        waybill_no: 运单号 (如 "SF1225198841659")
        from_ms: 开始时间戳(毫秒)
        to_ms: 结束时间戳(毫秒)
        limit: 返回行数上限

    返回: 日志列表
    """
    url, gs = grafana_session()

    # LogQL: 在所有服务中搜索运单号
    logql = f'{{app="fht-recycle"}} |= `{waybill_no}`'

    return grafana_loki_fetch(url, gs, logql, from_ms, to_ms, max_lines=limit)


def fetch_error_logs(service, from_ms, to_ms, limit=500):
    """
    查询错误日志

    参数:
        service: 服务名
        from_ms: 开始时间戳(毫秒)
        to_ms: 结束时间戳(毫秒)
        limit: 返回行数上限

    返回: 日志列表
    """
    url, gs = grafana_session()

    if service in SERVICE_MAP:
        job = SERVICE_MAP[service]["job"]
    else:
        job = f"prod-yhs/{service}"

    logql = f'{{job="{job}"}} |~ "(?i)(error|exception|fail)"'

    return grafana_loki_fetch(url, gs, logql, from_ms, to_ms, max_lines=limit)


def fetch_custom_logs(logql, from_ms, to_ms, limit=1000):
    """
    自定义 LogQL 查询

    参数:
        logql: 完整的 LogQL 表达式
        from_ms: 开始时间戳(毫秒)
        to_ms: 结束时间戳(毫秒)
        limit: 返回行数上限

    返回: 日志列表
    """
    url, gs = grafana_session()
    return grafana_loki_fetch(url, gs, logql, from_ms, to_ms, max_lines=limit)


# ============================================================
# 工具方法
# ============================================================
def filter_logs_by_keyword(logs, keyword):
    """
    在日志结果中按关键词二次过滤

    参数:
        logs: 日志列表
        keyword: 关键词

    返回: 过滤后的日志列表
    """
    return [log for log in logs if keyword in log["line"]]


def logs_to_json(logs, indent=2):
    """日志列表转 JSON 字符串"""
    return json.dumps(logs, ensure_ascii=False, indent=indent)


def print_logs(logs, max_count=50):
    """打印日志（限制条数）"""
    print(f"共 {len(logs)} 条日志" + (f"（显示前 {max_count} 条）" if len(logs) > max_count else ""))
    for log in logs[:max_count]:
        print(f"  [{log['timestamp']}] {log['line'][:200]}")


# ============================================================
# 命令行入口
# ============================================================
if __name__ == "__main__":
    import sys
    import time

    now_ms = int(time.time() * 1000)

    if len(sys.argv) < 2:
        print("用法:")
        print("  python grafana_loki.py <waybill_no> [hours]")
        print("  python grafana_loki.py SF1225198841659 1")
        sys.exit(1)

    waybill = sys.argv[1]
    hours = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    from_ms = now_ms - hours * 3600 * 1000

    print(f"查询运单号 {waybill} 最近 {hours} 小时的日志...")
    logs = fetch_waybill_logs(waybill, from_ms, now_ms)
    print_logs(logs)
