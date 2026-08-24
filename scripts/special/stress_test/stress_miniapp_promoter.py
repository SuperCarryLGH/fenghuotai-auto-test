"""
微信小程序分销拉新压测脚本

业务链路：
  A（推广官）: sms-login(无pid) -> dist/promoter/apply -> 后台自动审核 -> 实名 -> 签约 -> pid_A
  B（二级推广官）: sms-login(带pid_A) -> apply -> 后台自动审核 -> 实名 -> 签约 -> pid_B
  C（被拉新）: sms-login(带pid_B) 即完成（无 apply），可调钱包/查询接口

压测方式：三级渐进（基线/稳态/边界），安全阀自动停止，不压到崩溃。

环境：跟随 config.py 的 TEST_ENV（默认 dev），TEST_ENV=prod 时自动切到 prod。

运行方式：
    cd /Users/rs/PycharmProjects/PythonProject1
    TEST_ENV=dev .venv/bin/python scripts/special/stress_test/stress_miniapp_promoter.py
    TEST_ENV=prod .venv/bin/python scripts/special/stress_test/stress_miniapp_promoter.py

输出目录: scripts/special/stress_test/reports/
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

import csv
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests

from config import APP_URL, ADMIN_URL, ACCOUNTS
from Common.login import Login

# ============================================================
# 压测配置（按需修改）
# ============================================================
# 号段：A/B 推广官用 PROMOTER_PREFIX，C 被拉新用 NEW_PREFIX
# 注意：121/122 在 dev 被校验为"手机号格式不正确"，dev 用 156；prod 视校验规则调整
PROMOTER_PREFIX = os.getenv("PROMOTER_PREFIX", "140")   # A/B 推广官号段
NEW_PREFIX = os.getenv("NEW_PREFIX", "141")             # C 被拉新号段

# 并发梯度（基线/稳态/耐久/边界）
# 注意：P3耐久 并发建议跑完 P2 后按拐点填写（环境变量 SOAK_CONCURRENCY 覆盖）
SOAK_CONCURRENCY = int(os.getenv("SOAK_CONCURRENCY", "200"))
LEVELS = [
    {"name": "P1基线", "concurrency": 10, "duration": 60, "mix": {"bind": 0.6, "query": 0.4}},
    {"name": "P1基线", "concurrency": 50, "duration": 60, "mix": {"bind": 0.6, "query": 0.4}},
    {"name": "P2稳态", "concurrency": 100, "duration": 90, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P2稳态", "concurrency": 200, "duration": 90, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P2稳态", "concurrency": 400, "duration": 90, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P3耐久", "concurrency": SOAK_CONCURRENCY, "duration": 3600, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P4边界", "concurrency": 600, "duration": 60, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P4边界", "concurrency": 800, "duration": 60, "mix": {"bind": 0.7, "query": 0.3}},
    {"name": "P4边界", "concurrency": 1000, "duration": 60, "mix": {"bind": 0.7, "query": 0.3}},
]

# 安全阀
SAFETY_ERR_RATE = float(os.getenv("SAFETY_ERR_RATE", "2"))   # 错误率%阈值，超过自动停
SAFETY_P95_MS = float(os.getenv("SAFETY_P95_MS", "3000"))    # P95 ms 阈值
COOLDOWN_S = int(os.getenv("COOLDOWN_S", "30"))              # 档间回落时间（秒），观察系统恢复

# A/B 预置数量（动态扩展，跑多少造多少）
PRELOAD_A = int(os.getenv("PRELOAD_A", "5"))       # 预置推广官 A 数量
PRELOAD_B = int(os.getenv("PRELOAD_B", "20"))      # 预置二级推广官 B 数量

# 报告目录
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ============================================================
# Grafana 监控对接（拉取服务端指标，与本地压测数据合并）
# ============================================================
GRAFANA_FILE = os.path.join(PROJECT_ROOT, "Date", "Grafana.yaml")
GRAFANA_DATASOURCE_UID = "prometheus"   # Grafana 中 Prometheus 数据源 uid

# 监控指标清单（每档结束后拉取，与压测时段对齐）
GRAFANA_METRICS = {
    "node_cpu": 'sum by (instance) (rate(node_cpu_seconds_total{mode!="idle"}[1m])) * 100',
    "node_mem": '(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100',
    "node_disk": '(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100',
    "svc_cpu": 'sum by (service) (label_replace(rate(container_cpu_usage_seconds_total{namespace="prod-yhs"}[1m]), "service", "$1", "pod", "(.*)-[a-z0-9]{9,10}-[a-z0-9]{5}")) * 100',
    "svc_mem": 'sum by (service) (label_replace(container_memory_usage_bytes{namespace="prod-yhs"}, "service", "$1", "pod", "(.*)-[a-z0-9]{9,10}-[a-z0-9]{5}"))',
    "svc_net": 'sum by (service) (label_replace(rate(container_network_receive_bytes_total{namespace="prod-yhs"}[1m]), "service", "$1", "pod", "(.*)-[a-z0-9]{9,10}-[a-z0-9]{5}"))',
    "pod_restart": 'max by (service) (label_replace(kube_pod_container_status_restarts_total{namespace="prod-yhs"}, "service", "$1", "pod", "(.*)-[a-z0-9]{9,10}-[a-z0-9]{5}"))',
    "pod_status": 'sum by (phase) (kube_pod_status_phase{namespace="prod-yhs"})',
}

# ============================================================
# 全局状态（线程安全）
# ============================================================
_results_lock = threading.Lock()
_g = {
    "total": 0, "success": 0, "fail": 0, "times": [],
    "err_codes": {},
    "bind_total": 0, "bind_success": 0, "bind_times": [],
    "wallet_total": 0, "wallet_success": 0, "wallet_times": [],
    "pq_total": 0, "pq_success": 0, "pq_times": [],
    "tx_total": 0, "tx_success": 0, "tx_times": [],
    "trend": [],          # 每 10s 的 TPS/RT 快照 [(elapsed, tps, p95, err_rate), ...]
}

_g_mobile_seq = [0]
_g_mobile_used = set()
# 跨运行偏移基数：每次运行从随机大数起，避免与历史已注册号码冲突
_g_mobile_base = 10000000 + (int(time.time()) % 90000000)

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


# gen_mobile 安全上限：8位空间约 9000 万，超过上限报错避免死循环
_GEN_MOBILE_MAX_SEQ = 80000000


def gen_mobile(prefix):
    """动态生成不重复手机号：3位号段 + 8位递增数字（跨运行不撞历史号码）

    修复点：
      1. 旧实现 毫秒后3位+5位序号 同一毫秒取模会循环 → 高并发死循环
      2. 递增基数固定 10000000，进程重启后重新从 1 递增，
         会生成与历史已注册用户相同的手机号 → apply 报"推广员已开通"
      3. 8位取模极端溢出后撞号 → 死循环；加 seq 上限保护，超限报错
    新实现：基数基于运行时刻（随机大数），进程内单调递增 + set 去重，
    保证并发唯一且跨运行不撞已存在号码。
    """
    while True:
        _g_mobile_seq[0] += 1
        if _g_mobile_seq[0] > _GEN_MOBILE_MAX_SEQ:
            raise RuntimeError("gen_mobile 序号超上限，请调整号段或清理 _g_mobile_used")
        num = prefix + str(_g_mobile_base + _g_mobile_seq[0])[-8:]
        if len(num) == 11 and num not in _g_mobile_used:
            _g_mobile_used.add(num)
            return num


# ============================================================
# 登录工具
# ============================================================
def new_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0",
    })
    return s


def app_headers(token):
    return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}


def admin_headers(session):
    tok = Login(session=session).admin_login("admin")
    return {"tenant-id": "1", "appId": "admin", "sign": "admin",
            "Authorization": f"Bearer {tok}"}


def get_admin_headers(session, cached=None, force=False):
    """获取 admin headers，token 失效时自动重新登录（用户要求）"""
    if not force and cached is not None:
        return cached
    try:
        return admin_headers(session)
    except Exception:
        return admin_headers(session)  # 重试一次（临时网络抖动）


# ============================================================
# A/B 推广官注册（全流程，复用 dist 自动化审核逻辑）
# ============================================================
def register_promoter(session, mobile, promoter_id=None, admin_h=None):
    """sms-login -> apply -> (若未自动过审则 admin 审核) -> 实名 -> 签约 -> pid"""
    login = Login(session=session)
    if promoter_id:
        token = login.app_login_for_promoter(mobile=mobile, code="9999", promoter_id=promoter_id)
    else:
        token = login.app_login_with(mobile=mobile, code="9999")
    h = app_headers(token)
    body = {"mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
            "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
            "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
            "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
            "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
            "mediaScreenshot": ""}
    r = session.post(f"{APP_URL}/app-api/dist/promoter/apply", json=body,
                     headers=h, timeout=30).json()
    if r.get("code") != 0:
        raise RuntimeError(f"{mobile} apply 失败: {r.get('msg')}")
    # 若后台未自动过审（prod 可能需人工/自动审核），用 admin 审核
    if admin_h is not None:
        try:
            apply_id = r["data"].get("applyId")
            if apply_id:
                rg = session.get(f"{ADMIN_URL}/admin-api/dist/promoter-apply/get",
                                 params={"id": apply_id}, headers=admin_h, timeout=30).json()
                if rg.get("code") == 0 and isinstance(rg.get("data"), dict) \
                        and rg["data"].get("status") != 20:
                    upd = {**rg["data"], "status": 20}
                    session.put(f"{ADMIN_URL}/admin-api/dist/promoter-apply/update",
                                json=upd, headers=admin_h, timeout=30)
        except Exception:
            pass  # 审核失败不阻塞，dev 自动过审时无需 admin
    # 实名
    session.post(f"{APP_URL}/app-api/dist/promoter/real-name-auth",
                 json={"idCardFront": ID_CARD, "idCardBack": ID_CARD},
                 headers=h, timeout=30).json()
    # 签约
    session.post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                 json={"agreementUrl": "https://e.com/s.pdf"},
                 headers=h, timeout=30).json()
    # 拿 pid
    ri = session.get(f"{APP_URL}/app-api/dist/promoter/info", headers=h, timeout=30).json()
    if ri.get("code") != 0:
        raise RuntimeError(f"{mobile} 获取 pid 失败: {ri.get('msg')}")
    pid = ri["data"]["promoterId"]
    assert int(pid) > 0, f"{mobile} promoterId=0"
    return int(pid), token, h


# ============================================================
# Grafana 对接（拉取服务端监控指标）
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


def grafana_fetch(url, gs, expr, from_ms, to_ms):
    """调用 Grafana api/ds/query 拉取单个指标，返回 {label: [values]}"""
    payload = {
        "from": str(int(from_ms)), "to": str(int(to_ms)),
        "queries": [{"refId": "A", "datasource": {"uid": GRAFANA_DATASOURCE_UID, "type": "prometheus"},
                     "expr": expr}],
    }
    try:
        r = gs.post(f"{url}/api/ds/query", json=payload, timeout=30)
        data = r.json().get("results", {}).get("A", {})
        if data.get("error"):
            return {}
        frames = data.get("frames", [])
        out = {}
        for f in frames:
            fields = f.get("schema", {}).get("fields", [])
            if len(fields) < 2:
                continue
            # labels 在最后一个 field（Value）
            labels = fields[-1].get("labels", {}) or {}
            key = labels.get("instance") or labels.get("service") or labels.get("phase") or "value"
            vals = f.get("data", {}).get("values", []) or []
            # values 宽表结构: [[时间戳...], [数值...]]；无数据时 vals=[] 或 [[],[ ]]
            num_vals = vals[1] if len(vals) > 1 else []
            out[key] = [v for v in num_vals if v is not None]
        return out
    except Exception:
        return {}


def _stat(vals, func):
    return round(func(vals), 1) if vals else 0


def fetch_grafana_snapshot(from_ms, to_ms):
    """拉取所有监控指标快照，返回 {'指标名': {'均值':..,'峰值':..,'P95':.., '明细':{label:值}}}
    返回结构：
      {
        'node_cpu_avg': float, 'node_cpu_max': float, 'node_cpu_p95': float,
        ...
        'metrics_detail': {name: {label: [values]}}
      }
    """
    url, gs = grafana_session()
    res = {}
    detail = {}
    for name, expr in GRAFANA_METRICS.items():
        series = grafana_fetch(url, gs, expr, from_ms, to_ms)
        detail[name] = series
        all_vals = [v for vs in series.values() for v in vs]
        sorted_vals = sorted(all_vals)
        res[f"{name}_avg"] = round(sum(sorted_vals) / len(sorted_vals), 1) if sorted_vals else 0
        res[f"{name}_max"] = _stat(sorted_vals, max)
        res[f"{name}_p95"] = _stat(sorted_vals, lambda x: x[int(len(x) * 0.95)] if x else 0) if sorted_vals else 0
        res[f"{name}_p99"] = _stat(sorted_vals, lambda x: x[int(len(x) * 0.99)] if x else 0) if sorted_vals else 0
        res[f"{name}_count"] = len(series)
        # 内存类指标额外输出 GB 值（svc_mem 原始单位是字节）
        if name.endswith("_mem") or name == "svc_mem":
            res[f"{name}_gb"] = round(res[f"{name}_avg"] / (1024 ** 3), 2) if res[f"{name}_avg"] else 0
    res["metrics_detail"] = json.dumps(detail, ensure_ascii=False, default=str)
    return res


# ============================================================
# 压测操作（单次）
# ============================================================
def do_bind_login(session, mobile, pid_b, h_b_query):
    """C 被拉新：sms-login(带pid_B) + 钱包查询 + 钱包流水分页（3 次调用）"""
    login = Login(session=session)
    t0 = time.time()
    try:
        token = login.app_login_for_promoter(mobile=mobile, code="9999", promoter_id=pid_b)
        bind_elapsed = (time.time() - t0) * 1000
        h = app_headers(token)
        # 钱包查询
        t1 = time.time()
        rw = session.get(f"{APP_URL}/app-api/pay/wallet/get", headers=h, timeout=30)
        query_elapsed = (time.time() - t1) * 1000
        rw_json = rw.json()
        wallet_ok = rw_json.get("code") == 0
        # 钱包流水分页（独立统计，不参与整体成功判定）
        do_wallet_transaction_query(session, h)
        with _results_lock:
            _g["bind_total"] += 1
            _g["bind_times"].append(bind_elapsed)
            _g["bind_success"] += 1
            _g["wallet_total"] += 1
            _g["wallet_times"].append(query_elapsed)
            if wallet_ok:
                _g["wallet_success"] += 1
            # 绑定+钱包整体成功判定：绑定成功且钱包查询成功
            ok = wallet_ok
            _g["total"] += 1
            _g["times"].append(bind_elapsed + query_elapsed)
            if ok:
                _g["success"] += 1
            else:
                _g["fail"] += 1
                _g["err_codes"][f"wallet:{rw_json.get('code')}"] = _g["err_codes"].get(f"wallet:{rw_json.get('code')}", 0) + 1
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        with _results_lock:
            _g["bind_total"] += 1
            _g["bind_times"].append(elapsed)
            _g["total"] += 1
            _g["fail"] += 1
            _g["times"].append(elapsed)
            _g["err_codes"]["bind:" + str(type(e).__name__)] = _g["err_codes"].get("bind:" + str(type(e).__name__), 0) + 1


def do_promoter_query(session, h):
    """A/B 推广官查询：promoter/info + rule/get + 钱包流水分页"""
    t0 = time.time()
    try:
        r1 = session.get(f"{APP_URL}/app-api/dist/promoter/info", headers=h, timeout=30).json()
        r2 = session.get(f"{APP_URL}/app-api/dist/rule/get", params={"promoteType": 10},
                         headers=h, timeout=30).json()
        elapsed = (time.time() - t0) * 1000
        ok = r1.get("code") == 0 and r2.get("code") == 0
        # 钱包流水分页（独立统计，A/B 用自身 token）
        do_wallet_transaction_query(session, h)
        with _results_lock:
            _g["pq_total"] += 1
            _g["pq_times"].append(elapsed)
            _g["total"] += 1
            _g["times"].append(elapsed)
            if ok:
                _g["pq_success"] += 1
                _g["success"] += 1
            else:
                _g["fail"] += 1
                _g["err_codes"][f"query:{r1.get('code')}/{r2.get('code')}"] = \
                    _g["err_codes"].get(f"query:{r1.get('code')}/{r2.get('code')}", 0) + 1
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        with _results_lock:
            _g["pq_total"] += 1
            _g["pq_times"].append(elapsed)
            _g["total"] += 1
            _g["fail"] += 1
            _g["times"].append(elapsed)
            _g["err_codes"]["query:" + str(type(e).__name__)] = _g["err_codes"].get("query:" + str(type(e).__name__), 0) + 1


def do_wallet_transaction_query(session, h):
    """钱包流水分页查询：GET /app-api/pay/wallet-transaction/page（A/B/C 均可用自身 token）

    独立统计该接口的 RT/成功率，不参与 bind/pq 的整体成功判定。
    """
    t0 = time.time()
    try:
        r = session.get(f"{APP_URL}/app-api/pay/wallet-transaction/page",
                        params={"pageNo": 1, "pageSize": 10},
                        headers=h, timeout=30)
        elapsed = (time.time() - t0) * 1000
        rj = r.json()
        ok = rj.get("code") == 0
        with _results_lock:
            _g["tx_total"] += 1
            _g["tx_times"].append(elapsed)
            if ok:
                _g["tx_success"] += 1
            else:
                _g["err_codes"][f"wallet-tx:{rj.get('code')}"] = \
                    _g["err_codes"].get(f"wallet-tx:{rj.get('code')}", 0) + 1
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        with _results_lock:
            _g["tx_total"] += 1
            _g["tx_times"].append(elapsed)
            _g["err_codes"]["wallet-tx:" + str(type(e).__name__)] = \
                _g["err_codes"].get("wallet-tx:" + str(type(e).__name__), 0) + 1


# ============================================================
# 指标统计
# ============================================================
def pct(sorted_times, p):
    if not sorted_times:
        return 0
    idx = min(len(sorted_times) - 1, int(len(sorted_times) * p))
    return sorted_times[idx]


def snapshot(name, duration, concurrency=None):
    with _results_lock:
        total = _g["total"]; success = _g["success"]; fail = _g["fail"]
        times = sorted(_g["times"])
        bind_times = sorted(_g["bind_times"])
        wallet_times = sorted(_g["wallet_times"])
        pq_times = sorted(_g["pq_times"])
        tx_times = sorted(_g["tx_times"])
        err_codes = dict(_g["err_codes"])
        bind_total = _g["bind_total"]; query_total = _g["wallet_total"] + _g["pq_total"]
        tx_total = _g["tx_total"]
        trend = list(_g["trend"])
    tps = total / duration if duration > 0 else 0
    err_rate = fail / total * 100 if total else 0
    # 分链路 QPS
    bind_qps = bind_total / duration if duration > 0 else 0
    wallet_qps = _g["wallet_total"] / duration if duration > 0 else 0
    pq_qps = _g["pq_total"] / duration if duration > 0 else 0
    tx_qps = tx_total / duration if duration > 0 else 0
    row = {
        "level": name,
        "concurrency": concurrency if concurrency is not None else "",
        "duration": round(duration, 1),
        "total": total,
        "success": success,
        "fail": fail,
        "err_rate": round(err_rate, 2),
        "tps": round(tps, 1),
        "bind_qps": round(bind_qps, 1),
        "wallet_qps": round(wallet_qps, 1),
        "pq_qps": round(pq_qps, 1),
        "tx_qps": round(tx_qps, 1),
        "tx_total": tx_total,
        "tx_p95": round(pct(tx_times, 0.95), 0),
        "p50": round(pct(times, 0.50), 0),
        "p95": round(pct(times, 0.95), 0),
        "p99": round(pct(times, 0.99), 0),
        "p999": round(pct(times, 0.999), 0),
        "max_rt": round(times[-1], 0) if times else 0,
        "bind_p95": round(pct(bind_times, 0.95), 0),
        "wallet_p95": round(pct(wallet_times, 0.95), 0),
        "pq_p95": round(pct(pq_times, 0.95), 0),
        "trend": json.dumps(trend, ensure_ascii=False),
        "err_codes": json.dumps(err_codes, ensure_ascii=False),
    }
    return row


def print_row(row):
    print(f"  {row['level']:8s} 并发:{row.get('concurrency', row['total']):>6} 请求:{row['total']:>7d} "
          f"成功:{row['success']:>7d} 失败:{row['fail']:>5d} 错误率:{row['err_rate']:>5.2f}% "
          f"TPS:{row['tps']:>7.1f} P50:{row['p50']:>6.0f}ms "
          f"P95:{row['p95']:>6.0f}ms P99:{row['p99']:>6.0f}ms")


# ============================================================
# 单档并发执行
# ============================================================
def run_level(session, ah, level, pid_b_pool, promoter_h_pool):
    """执行一个并发梯度，返回统计行"""
    concurrency = level["concurrency"]
    duration = level["duration"]
    mix = level["mix"]
    name = level["name"]

    # 重置本档计数
    with _results_lock:
        _g["total"] = _g["success"] = _g["fail"] = 0
        _g["times"] = []
        _g["bind_total"] = _g["bind_success"] = _g["wallet_total"] = _g["wallet_success"] = 0
        _g["bind_times"] = _g["wallet_times"] = _g["pq_times"] = []
        _g["pq_total"] = _g["pq_success"] = 0
        _g["tx_total"] = _g["tx_success"] = 0
        _g["tx_times"] = []
        _g["err_codes"] = {}
        _g["trend"] = []

    print(f"\n  --- {name} 并发={concurrency} 时长={duration}s ---")

    def worker(_):
        # 池空保护：避免 random.choice 抛 IndexError 中断压测
        if not pid_b_pool or not promoter_h_pool:
            return
        s = new_session()
        # 随机决策：绑定登录(C) or 推广官查询(A/B)
        if random.random() < mix["bind"]:
            pid_b = random.choice(pid_b_pool)
            mobile = gen_mobile(NEW_PREFIX)
            do_bind_login(s, mobile, pid_b, None)
        else:
            h = random.choice(promoter_h_pool)
            do_promoter_query(s, h)

    start = time.time()
    start_ms = int(start * 1000)

    # 趋势采样 + 实时熔断线程
    _trend_stop = [False]
    _circuit = [False]          # 实时熔断标志：错误率/P95 超阈值则置 True
    _circuit_reason = [""]

    def _trend_sampler():
        last_total = 0
        last_ts = start
        while not _trend_stop[0]:
            # 拆短 sleep 间隔，保证 stop 后能及时退出（避免串档）
            for _ in range(20):
                if _trend_stop[0]:
                    return
                time.sleep(0.5)
            with _results_lock:
                cur_total = _g["total"]
                cur_times = sorted(_g["times"])
                cur_fail = _g["fail"]
            now = time.time()
            interval = now - last_ts
            tps = (cur_total - last_total) / interval if interval > 0 else 0
            p95 = pct(cur_times, 0.95) if cur_times else 0
            err_rate = cur_fail / cur_total * 100 if cur_total else 0
            _g["trend"].append({
                "elapsed": round(now - start, 1),
                "tps": round(tps, 1),
                "p95": round(p95, 0),
                "err_rate": round(err_rate, 2),
            })
            # 实时熔断：趋势采样窗口内错误率/P95 超阈值即中断本档
            if err_rate > SAFETY_ERR_RATE:
                _circuit[0] = True
                _circuit_reason[0] = f"实时错误率 {err_rate}% > {SAFETY_ERR_RATE}%"
            elif p95 > SAFETY_P95_MS:
                _circuit[0] = True
                _circuit_reason[0] = f"实时P95 {p95}ms > {SAFETY_P95_MS}ms"
            last_total = cur_total
            last_ts = now

    trend_thread = threading.Thread(target=_trend_sampler, daemon=True)
    trend_thread.start()

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = []
        deadline = start + duration
        while time.time() < deadline:
            if _circuit[0]:
                print(f"  ⛔ 实时熔断触发: {_circuit_reason[0]}，停止提交新请求")
                break
            futures.append(pool.submit(worker, None))
            # 控制提交速率，避免堆积过多（生产者-消费者）
            while len(futures) > concurrency * 3:
                done = {f for f in futures if f.done()}
                futures = [f for f in futures if f not in done]
                time.sleep(0.01)
        # 等待剩余完成
        for f in as_completed(futures):
            pass
    _trend_stop[0] = True
    trend_thread.join(timeout=5)
    elapsed = time.time() - start
    end_ms = int(time.time() * 1000)

    row = snapshot(name, elapsed, concurrency=concurrency)

    # 拉取 Grafana 服务端监控快照（与本档压测时段对齐）
    print("      拉取 Grafana 服务端监控...")
    try:
        gs_snap = fetch_grafana_snapshot(start_ms, end_ms)
        row.update(gs_snap)
        print(f"      Node CPU avg={gs_snap.get('node_cpu_avg')}% 服务CPU avg={gs_snap.get('svc_cpu_avg')}% "
              f"服务内存avg={gs_snap.get('svc_mem_avg')}")
    except Exception as e:
        print(f"      ⚠ Grafana 拉取失败: {e}")

    # 安全阀判断（含实时熔断信号）
    trip = False
    reason = ""
    if _circuit[0]:
        trip = True; reason = _circuit_reason[0]
    if row["err_rate"] > SAFETY_ERR_RATE:
        trip = True; reason = f"错误率 {row['err_rate']}% > {SAFETY_ERR_RATE}%"
    if row["p95"] > SAFETY_P95_MS:
        trip = True; reason = f"P95 {row['p95']}ms > {SAFETY_P95_MS}ms"
    row["interrupted"] = "是" if trip else ""
    row["stop_reason"] = reason
    print_row(row)
    if row["err_codes"]:
        print(f"      错误分布: {row['err_codes']}")
    if trip:
        print(f"  ⛔ 安全阀触发: {reason}，本档中断")
    return row, trip, reason


# ============================================================
# HTML 报告导出（ECharts 折线趋势图）
# ============================================================
def export_html_report(results, path):
    """生成带 ECharts 折线趋势图的 HTML 压测报告"""
    # 解析每档的 trend 数据
    series_tps = []       # {name, points: [[elapsed, tps], ...]}
    series_p95 = []
    series_err = []
    summary_rows = []
    for r in results:
        try:
            trend_data = json.loads(r.get("trend") or "[]")
        except Exception:
            trend_data = []
        name = f"{r['level']}(并发{r.get('concurrency','')})"
        pts_tps = [[t.get("elapsed"), t.get("tps")] for t in trend_data]
        pts_p95 = [[t.get("elapsed"), t.get("p95")] for t in trend_data]
        pts_err = [[t.get("elapsed"), t.get("err_rate")] for t in trend_data]
        if pts_tps:
            series_tps.append({"name": name, "points": pts_tps})
            series_p95.append({"name": name, "points": pts_p95})
            series_err.append({"name": name, "points": pts_err})
        summary_rows.append(r)

    # 汇总表 HTML
    head = (f"<th>阶段</th><th>并发</th><th>总请求</th><th>成功</th><th>失败</th><th>错误率</th>"
            f"<th>TPS</th><th>P50</th><th>P95</th><th>P99</th><th>P999</th><th>MaxRT</th>"
            f"<th>绑定QPS</th><th>钱包QPS</th><th>查询QPS</th>"
            f"<th>NodeCPU%</th><th>服务CPU%</th><th>服务内存G</th><th>中断</th>")
    rows_html = ""
    for r in summary_rows:
        rows_html += (
            f"<tr><td>{r.get('level')}</td><td>{r.get('concurrency','')}</td>"
            f"<td>{r.get('total')}</td><td>{r.get('success')}</td><td>{r.get('fail')}</td>"
            f"<td>{r.get('err_rate')}%</td><td>{r.get('tps')}</td>"
            f"<td>{r.get('p50')}</td><td>{r.get('p95')}</td><td>{r.get('p99')}</td>"
            f"<td>{r.get('p999')}</td><td>{r.get('max_rt')}</td>"
            f"<td>{r.get('bind_qps')}</td><td>{r.get('wallet_qps')}</td><td>{r.get('pq_qps')}</td>"
            f"<td>{r.get('node_cpu_avg')}</td><td>{r.get('svc_cpu_avg')}</td><td>{r.get('svc_mem_gb')}</td>"
            f"<td>{r.get('interrupted') or '-'}{' '+str(r.get('stop_reason')) if r.get('stop_reason') else ''}</td></tr>"
        )

    tps_series = ", ".join(
        f'{{name:"{s["name"]}", type:"line", smooth:true, data:{json.dumps(s["points"])}}}' for s in series_tps)
    p95_series = ", ".join(
        f'{{name:"{s["name"]}", type:"line", smooth:true, data:{json.dumps(s["points"])}}}' for s in series_p95)
    err_series = ", ".join(
        f'{{name:"{s["name"]}", type:"line", smooth:true, data:{json.dumps(s["points"])}}}' for s in series_err)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>微信小程序分销拉新压测报告</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; margin: 20px; color: #333; }}
h2 {{ color: #1a1a1a; }}
.meta {{ color: #888; font-size: 13px; margin-bottom: 20px; }}
.card {{ background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
.chart {{ width: 100%; height: 400px; }}
table {{ border-collapse: collapse; font-size: 13px; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: right; white-space: nowrap; }}
th {{ background: #f5f5f5; position: sticky; top: 0; }}
tr:nth-child(even) {{ background: #fafafa; }}
</style>
</head>
<body>
<h2>微信小程序分销拉新压测报告</h2>
<p class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 环境: {APP_URL} | 场景: 分销拉新登录（A/B推广官 + C被拉新）</p>

<div class="card">
<h3>一、压测汇总</h3>
<div style="overflow-x:auto">
<table>
<thead><tr>{head}</tr></thead>
<tbody>{rows_html}</tbody>
</table>
</div>
</div>

<div class="card">
<h3>二、TPS 趋势（每 10s）</h3>
<div id="chart_tps" class="chart"></div>
</div>

<div class="card">
<h3>三、P95 响应时间趋势（每 10s）</h3>
<div id="chart_p95" class="chart"></div>
</div>

<div class="card">
<h3>四、错误率趋势（每 10s）</h3>
<div id="chart_err" class="chart"></div>
</div>

<script>
function makeChart(id, title, yName, series) {{
  var chart = echarts.init(document.getElementById(id));
  chart.setOption({{
    title: {{ text: title, left: 'center', textStyle: {{ fontSize: 14 }} }},
    tooltip: {{ trigger: 'axis' }},
    legend: {{ bottom: 0, type: 'scroll' }},
    grid: {{ left: 60, right: 30, top: 50, bottom: 40 }},
    xAxis: {{ type: 'value', name: '时间(s)', minInterval: 1 }},
    yAxis: {{ type: 'value', name: yName }},
    series: series
  }});
}}
makeChart('chart_tps', 'TPS 趋势', 'TPS', [{tps_series}]);
makeChart('chart_p95', 'P95 响应时间趋势', 'RT(ms)', [{p95_series}]);
makeChart('chart_err', '错误率趋势', '错误率(%)', [{err_series}]);
window.addEventListener('resize', function(){{
  echarts.init(document.getElementById('chart_tps')).resize();
  echarts.init(document.getElementById('chart_p95')).resize();
  echarts.init(document.getElementById('chart_err')).resize();
}});
</script>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("微信小程序分销拉新压测")
    print(f"环境: {APP_URL}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 0) 管理员登录
    print("\n[0/5] 管理员登录...")
    session = new_session()
    try:
        ah = get_admin_headers(session)
        print("  admin 登录成功")
    except Exception as e:
        print(f"[ERROR] admin 登录失败: {e}")
        print("[ERROR] 请检查 ACCOUNTS 配置/网络，压测终止")
        return

    # 1) 预置推广官 A
    print(f"\n[1/5] 预置推广官 A（{PRELOAD_A} 个）...")
    pid_a_pool = []
    for i in range(PRELOAD_A):
        try:
            mb = gen_mobile(PROMOTER_PREFIX)
            pid, _, _ = register_promoter(session, mb, admin_h=ah)
            pid_a_pool.append(pid)
            print(f"  A[{i+1}] {mb} -> pid={pid}")
        except Exception as e:
            # admin token 可能失效，刷新后重试一次
            if "登录" in str(e) or "Unauthorized" in str(e) or "401" in str(e):
                ah = get_admin_headers(session, force=True)
                try:
                    mb = gen_mobile(PROMOTER_PREFIX)
                    pid, _, _ = register_promoter(session, mb, admin_h=ah)
                    pid_a_pool.append(pid)
                    print(f"  A[{i+1}] {mb} -> pid={pid} (admin刷新后重试成功)")
                    continue
                except Exception as e2:
                    print(f"  A[{i+1}] 刷新后仍失败: {e2}")
            else:
                print(f"  A[{i+1}] 注册失败: {e}")
    if not pid_a_pool:
        print("[ERROR] 无可用 A 推广官，退出")
        return
    print(f"  共 {len(pid_a_pool)} 个 A")

    # 2) 预置推广官 B（绑定随机 A）
    print(f"\n[2/5] 预置推广官 B（{PRELOAD_B} 个）...")
    pid_b_pool = []
    b_mobiles = []
    for i in range(PRELOAD_B):
        try:
            mb = gen_mobile(PROMOTER_PREFIX)
            pid_a = random.choice(pid_a_pool)
            pid, token, h = register_promoter(session, mb, promoter_id=pid_a, admin_h=ah)
            pid_b_pool.append(pid)
            b_mobiles.append((pid, token, h))
            print(f"  B[{i+1}] {mb} -> pid={pid} (父={pid_a})")
        except Exception as e:
            if "登录" in str(e) or "Unauthorized" in str(e) or "401" in str(e):
                ah = get_admin_headers(session, force=True)
                try:
                    mb = gen_mobile(PROMOTER_PREFIX)
                    pid_a = random.choice(pid_a_pool)
                    pid, token, h = register_promoter(session, mb, promoter_id=pid_a, admin_h=ah)
                    pid_b_pool.append(pid)
                    b_mobiles.append((pid, token, h))
                    print(f"  B[{i+1}] {mb} -> pid={pid} (admin刷新后重试成功)")
                    continue
                except Exception as e2:
                    print(f"  B[{i+1}] 刷新后仍失败: {e2}")
            else:
                print(f"  B[{i+1}] 注册失败: {e}")
    if not pid_b_pool:
        print("[ERROR] 无可用 B 推广官，退出")
        return
    promoter_h_pool = [h for _, _, h in b_mobiles]
    print(f"  共 {len(pid_b_pool)} 个 B")

    # 3) 压测执行
    print("\n[3/5] 开始压测...")
    results = []
    stopped = False
    for level in LEVELS:
        row, trip, reason = run_level(session, ah, level, pid_b_pool, promoter_h_pool)
        results.append(row)
        # 档间回落，观察系统恢复（防下档叠加压力）
        if not trip:
            print(f"  档间回落 {COOLDOWN_S}s，观察系统恢复...")
            time.sleep(COOLDOWN_S)
        else:
            stopped = True
            break

    # 4) 汇总输出
    print("\n[4/5] 汇总:")
    print("  " + "-" * 150)
    header = (f"  {'阶段':8s} {'并发':>5s} {'总请求':>7s} {'错误率':>7s} {'TPS':>7s} "
              f"{'P50':>6s} {'P95':>6s} {'P99':>6s} {'P999':>6s} {'绑定QPS':>7s} {'钱包QPS':>7s} {'查询QPS':>7s} {'流水QPS':>7s} "
              f"{'NodeCPU':>8s} {'SvcCPU':>8s} {'SvcMemG':>7s} {'中断':>4s}")
    print(header)
    print("  " + "-" * 150)
    for r in results:
        print(f"  {r['level']:8s} {r.get('concurrency',''):>5} {r['total']:>7d} "
              f"{r['err_rate']:>6.2f}% {r['tps']:>7.1f} {r['p50']:>5.0f} {r['p95']:>5.0f} "
              f"{r['p99']:>5.0f} {r['p999']:>5.0f} {r['bind_qps']:>7.1f} {r['wallet_qps']:>7.1f} "
              f"{r['pq_qps']:>7.1f} {r.get('tx_qps', 0):>7.1f} "
              f"{r.get('node_cpu_avg', 0):>7.1f}% {r.get('svc_cpu_avg', 0):>7.1f}% {r.get('svc_mem_gb', 0):>7.2f} "
              f"{r.get('interrupted', '') or '-':>4s}")
    print("  " + "-" * 150)

    # 5) 报告导出（主汇总 + 趋势明细 + 明细 JSON）
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(REPORT_DIR, f"miniapp_promoter_{ts}.csv")
        # 主 CSV 剔除 trend / metrics_detail（避免单格过大），分别单独导出
        main_cols = [k for k in results[0].keys() if k not in ("trend", "metrics_detail")]
        with open(report_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=main_cols)
            writer.writeheader()
            for r in results:
                writer.writerow({k: r[k] for k in main_cols})
        print(f"\n[5/5] 汇总报告已导出: {report_path}")

        # 趋势明细（每档每 10s 的 TPS/RT）
        trend_path = os.path.join(REPORT_DIR, f"miniapp_promoter_{ts}_trend.csv")
        with open(trend_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["level", "concurrency", "elapsed_s", "tps", "p95_ms", "err_rate"])
            for r in results:
                try:
                    trend_data = json.loads(r.get("trend") or "[]")
                except Exception:
                    trend_data = []
                for t in trend_data:
                    writer.writerow([r["level"], r.get("concurrency", ""),
                                     t.get("elapsed"), t.get("tps"), t.get("p95"), t.get("err_rate")])
        print(f"  趋势明细已导出: {trend_path}")

        # 服务端明细 JSON（完整序列，供深入分析）
        detail_path = os.path.join(REPORT_DIR, f"miniapp_promoter_{ts}_metrics.json")
        with open(detail_path, "w", encoding="utf-8") as f:
            detail_out = []
            for r in results:
                try:
                    detail_out.append({"level": r["level"], "concurrency": r.get("concurrency"),
                                       "metrics": json.loads(r.get("metrics_detail") or "{}")})
                except Exception:
                    pass
            json.dump(detail_out, f, ensure_ascii=False, indent=2, default=str)
        print(f"  服务端明细已导出: {detail_path}")

        # HTML 折线趋势图报告
        html_path = os.path.join(REPORT_DIR, f"miniapp_promoter_{ts}.html")
        export_html_report(results, html_path)
        print(f"  HTML 趋势图报告已导出: {html_path}")
    except Exception as e:
        print(f"  ⚠ 报告导出失败（不影响压测结果数据，可手动查看控制台输出）: {e}")
    print(f"\n压测完成" + ("（安全阀中断）" if stopped else ""))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] 压测被手动终止 (Ctrl+C)")
    except Exception as e:
        import traceback
        print("\n" + "=" * 60)
        print("[ERROR] 压测异常终止")
        print(f"  错误: {e}")
        traceback.print_exc()
        print("=" * 60)
        raise