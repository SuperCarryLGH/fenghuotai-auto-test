"""
用户提现压测脚本

运行方式:
    cd /Users/rs/PycharmProjects/PythonProject1
    python -m Testcase.stress_test.stress_withdraw

输出目录: Testcase/stress_test/reports/
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

import csv
import json
import time
import uuid
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime

import requests
from config import ADMIN_URL
from Common.login import Login
from Common.loader import load_yaml

# ============================================================
# 压测配置（按需修改）
# ============================================================
USE_GATEWAY = True          # True=走网关  False=直连pay-server实例（测裸机上限）
USE_MOCK = True            # True=内存mock（不调真实接口，纯逻辑压测）

PAY_INSTANCES = [
    # 直连时填写 pay-server 实例地址，格式: "http://IP:端口"
    # 多个实例会随机轮询
    # "http://10.0.0.1:48080",   # pay-server 实例1
    # "http://10.0.0.2:48080",   # pay-server 实例2
]

# ============================================================
# 全局变量
# ============================================================
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ============================================================
# Mock 内存钱包（USE_MOCK=True 时启用）
# ============================================================
_mock_wallets = {}          # {userId: balance}    内存余额表
_mock_lock = threading.Lock()

_original_post = requests.post
_original_get = requests.get


def _build_mock_resp(status_code: int, data: dict) -> "requests.Response":
    from unittest.mock import MagicMock
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = data
    return resp


def _mock_post(url, **kwargs):
    if not USE_MOCK:
        return _original_post(url, **kwargs)

    json_body = kwargs.get("json", {})

    # --- 登录 mock ---
    if "auth/login" in url or "sms-login" in url:
        return _build_mock_resp(200, {"code": 0, "msg": "", "data": {"accessToken": "mock_stress_token"}})

    # --- 充值 ---
    if "charge-operate-fund" in url:
        org_id = json_body.get("orgId", 0)
        amount = json_body.get("rechargeAmount", 0)
        with _mock_lock:
            _mock_wallets[org_id] = _mock_wallets.get(org_id, 0) + amount
        return _build_mock_resp(200, {"code": 0, "msg": "", "data": True})

    # --- 提现 ---
    if "withdraw-operate-fund" in url:
        org_id = json_body.get("orgId", 0)
        amount = json_body.get("amount", 0)
        with _mock_lock:
            current = _mock_wallets.get(org_id, 0)
            if current >= amount:
                _mock_wallets[org_id] = current - amount
                return _build_mock_resp(200, {"code": 0, "msg": "", "data": True})
            else:
                return _build_mock_resp(200, {"code": 500, "msg": "余额不足", "data": False})

    # --- 其他 POST ---
    return _build_mock_resp(200, {"code": 0, "msg": "", "data": True})


def _mock_get(url, **kwargs):
    if not USE_MOCK:
        return _original_get(url, **kwargs)

    params = kwargs.get("params", {})

    # --- 查钱包 ---
    if "wallet/page" in url:
        user_id = int(params.get("userId", 0))
        mobile = params.get("mobile", "")
        with _mock_lock:
            balance = _mock_wallets.get(user_id, 0)
        return _build_mock_resp(200, {
            "code": 0, "msg": "", "data": {
                "total": 1, "list": [{
                    "userId": user_id, "walletId": user_id,
                    "balance": balance, "freezePrice": 0,
                }]
            }
        })

    # --- 查流水 ---
    if "walletTranPage" in url or "fund-flow/page" in url:
        return _build_mock_resp(200, {"code": 0, "msg": "", "data": {"total": 0, "list": []}})

    # --- 其他 GET ---
    return _build_mock_resp(200, {"code": 0, "msg": "", "data": {}})


if USE_MOCK:
    requests.post = _mock_post
    requests.get = _mock_get
    requests.Session.post = lambda self, url, **kw: _mock_post(url, **kw)
    requests.Session.get = lambda self, url, **kw: _mock_get(url, **kw)
    print("[MOCK] 已启用内存 Mock，不调真实接口")
# ============================================================


def pay_base_url() -> str:
    """获取 pay RPC 接口的 base URL（网关 or 直连实例）"""
    if not USE_GATEWAY and PAY_INSTANCES:
        return random.choice(PAY_INSTANCES)
    return ADMIN_URL


# Admin 接口（查钱包/流水）始终走网关
WALLET_PAGE_URL = f"{ADMIN_URL}/admin-api/pay/wallet/page"
TRANSACTION_PAGE_URL = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/walletTranPage"
FUND_FLOW_PAGE_URL = f"{ADMIN_URL}/admin-api/pay/fund-flow/page"

results_lock = threading.Lock()
total_requests = 0
success_count = 0
fail_count = 0
response_times = []


@dataclass
class WalletInfo:
    mobile: str
    userId: int
    walletId: int
    balance: int
    freezePrice: int

    @property
    def available(self) -> int:
        return self.balance - self.freezePrice


# ============================================================
# HTTP 工具
# ============================================================
def build_admin_headers() -> dict:
    login = Login()
    token = login.admin_login("operator")
    return {
        "Content-Type": "application/json",
        "tenant-id": "1",
        "Authorization": f"Bearer {token}",
    }


def api_get(url: str, params: dict, headers: dict) -> dict:
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def api_post(url: str, payload: dict, headers: dict) -> dict:
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ============================================================
# 准备阶段
# ============================================================
def setup_users(headers: dict) -> list[WalletInfo]:
    """读取 batch_users.yaml，登录每个用户，查询钱包信息"""
    data = load_yaml("batch_users.yaml")
    mobiles = [u["mobile"] for u in data.get("batch_users", [])]

    wallets = []
    for mobile in mobiles:
        # 登录触发自动注册
        login = Login()
        login.app_login_with(mobile=mobile, code="9999")

        # 查钱包
        resp = api_get(WALLET_PAGE_URL, {"walletType": "40", "mobile": mobile, "pageNo": 1, "pageSize": 1}, headers)
        items = resp.get("data", {}).get("list", [])
        if items:
            w = items[0]
            wallet = WalletInfo(
                mobile=mobile,
                userId=w["userId"],
                walletId=w["walletId"],
                balance=w["balance"],
                freezePrice=w.get("freezePrice", 0),
            )
            wallets.append(wallet)
            print(f"  ✅ {mobile} | userId={wallet.userId} | walletId={wallet.walletId} | balance={wallet.balance}")
        else:
            print(f"  ⚠️ {mobile} 未找到钱包")

    return wallets


def recharge_wallets(wallets: list[WalletInfo], target_amounts: dict[int, int], headers: dict):
    """为钱包充值到目标余额"""
    for w in wallets:
        current = w.available
        target = target_amounts.get(w.userId, current)
        if current >= target:
            print(f"  ✅ {w.mobile} 余额充足: {current} >= {target}，跳过充值")
            continue

        need = target - current
        print(f"  💰 {w.mobile} 充值 {need} 分 ... ", end="", flush=True)
        biz_no = f"STRESS_{uuid.uuid4().hex[:16]}"
        payload = {
            "orgId": w.userId,
            "tradeChannel": 1,
            "rechargeAmount": need,
            "thirdNo": biz_no,
            "bizNo": biz_no,
        }
        resp = api_post(f"{pay_base_url()}/rpc-api/pay/pay/charge-operate-fund", payload, headers)
        if resp.get("code") == 0:
            w.balance = target
            print("OK")
        else:
            print(f"FAIL → {resp.get('msg')}")

    # 等待到账
    time.sleep(2)


# ============================================================
# 提现请求（单次）
# ============================================================
def do_withdraw(headers: dict, wallet: WalletInfo, amount: int) -> dict:
    """单次提现, 返回响应 dict"""
    global total_requests, success_count, fail_count

    start = time.time()
    biz_no = f"WD_{uuid.uuid4().hex[:16]}"
    payload = {
        "withdrawalType": 2,  # 用户提现
        "orgId": wallet.userId,
        "amount": amount,
        "bizNo": biz_no,
        "thirdOrderNo": biz_no,
        "tradeChannel": 1,
    }
    try:
        resp = api_post(f"{pay_base_url()}/rpc-api/pay/pay/withdraw-operate-fund", payload, headers)
        elapsed = (time.time() - start) * 1000
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        resp = {"code": -1, "msg": str(e), "data": False}

    with results_lock:
        total_requests += 1
        response_times.append(elapsed)
        if resp.get("code") == 0 and resp.get("data") is True:
            success_count += 1
        else:
            fail_count += 1

    return resp


# ============================================================
# 场景一：防超扣
# ============================================================
def scenario_anti_oversubtraction(headers: dict, wallets: list[WalletInfo]):
    print("\n" + "=" * 60)
    print("场景一：防超扣验证")
    print("=" * 60)

    test_users = wallets[:10]
    # 每个用户余额设为 1 分
    recharge_wallets(test_users, {w.userId: 1 for w in test_users}, headers)

    # 刷新余额
    test_users = refresh_balances(test_users, headers)
    for u in test_users:
        print(f"  📋 {u.mobile} 可用余额: {u.available} 分")

    print(f"\n  启动 50 线程并发提现（每次 1 分）...")
    global total_requests, success_count, fail_count, response_times
    total_requests = success_count = fail_count = 0
    response_times = []

    start = time.time()
    with ThreadPoolExecutor(max_workers=50) as pool:
        futures = []
        for _ in range(50):
            user = random.choice(test_users)
            futures.append(pool.submit(do_withdraw, headers, user, 1))
        for f in as_completed(futures):
            pass
    elapsed = time.time() - start

    print(f"\n  结果:")
    print(f"    总请求: {total_requests}")
    print(f"    成功: {success_count}  (期望: {len(test_users)})")
    print(f"    失败: {fail_count}  (期望: {total_requests - len(test_users)})")
    print(f"    耗时: {elapsed:.1f}s")
    print(f"    P99: {sorted(response_times)[int(len(response_times) * 0.99)]:.0f}ms" if response_times else "    P99: N/A")

    if success_count == len(test_users) and success_count + fail_count == total_requests:
        print("  ✅ 防超扣验证通过：没有超发")
    else:
        print(f"  ❌ 防超扣验证失败：预期 {len(test_users)} 成功，实际 {success_count}")


# ============================================================
# 场景二：吞吐量压测
# ============================================================
def scenario_throughput(headers: dict, wallets: list[WalletInfo]):
    print("\n" + "=" * 60)
    print("场景二：吞吐量压测")
    print("=" * 60)

    test_users = wallets[:20]
    # 每用户充 10000 分
    recharge_wallets(test_users, {w.userId: 10000 for w in test_users}, headers)

    global total_requests, success_count, fail_count, response_times

    concurrency_levels = [10, 50, 100, 200]
    if len(test_users) == 1:
        concurrency_levels = [5, 10, 20, 50]

    print(f"\n  {'并发数':>6} | {'请求数':>6} | {'成功':>6} | {'失败':>6} | {'耗时':>6} | {'TPS':>8} | {'P99(ms)':>8}")
    print("  " + "-" * 65)

    for concurrency in concurrency_levels:
        total_requests = success_count = fail_count = 0
        response_times = []

        start = time.time()
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = []
            deadline = start + 30
            while time.time() < deadline:
                user = random.choice(test_users)
                futures.append(pool.submit(do_withdraw, headers, user, 100))
            for f in as_completed(futures):
                pass
        elapsed = time.time() - start

        tps = total_requests / elapsed if elapsed > 0 else 0
        p99 = sorted(response_times)[int(len(response_times) * 0.99)] if response_times else 0
        print(f"  {concurrency:>6} | {total_requests:>6} | {success_count:>6} | {fail_count:>6} | {elapsed:>5.1f}s | {tps:>7.1f} | {p99:>8.0f}")


# ============================================================
# 场景三：混合压测
# ============================================================
def scenario_mixed(headers: dict, wallets: list[WalletInfo]):
    print("\n" + "=" * 60)
    print("场景三：混合压测（模拟真实流量）")
    print("=" * 60)

    test_users = wallets[:20]
    # 20% 余额只够 1 次，80% 余额充裕
    low_balance_count = max(1, len(test_users) // 5)
    low_users = test_users[:low_balance_count]
    high_users = test_users[low_balance_count:]

    recharge_wallets(low_users, {w.userId: 1 for w in low_users}, headers)
    recharge_wallets(high_users, {w.userId: 10000 for w in high_users}, headers)

    global total_requests, success_count, fail_count, response_times
    total_requests = success_count = fail_count = 0
    response_times = []

    print(f"  低余额用户 ({len(low_users)} 个): " + ", ".join(u.mobile for u in low_users))
    print(f"  高余额用户 ({len(high_users)} 个): " + ", ".join(u.mobile for u in high_users))
    print(f"\n  启动 100 线程混合压测 60 秒...")

    start = time.time()
    with ThreadPoolExecutor(max_workers=100) as pool:
        futures = []
        deadline = start + 60
        while time.time() < deadline:
            if random.random() < 0.2:
                user = random.choice(low_users)
            else:
                user = random.choice(high_users)
            futures.append(pool.submit(do_withdraw, headers, user, 100))
        for f in as_completed(futures):
            pass
    elapsed = time.time() - start

    tps = total_requests / elapsed if elapsed > 0 else 0
    p99 = sorted(response_times)[int(len(response_times) * 0.99)] if response_times else 0

    print(f"\n  结果:")
    print(f"    总请求: {total_requests}")
    print(f"    成功: {success_count}")
    print(f"    失败: {fail_count}")
    print(f"    耗时: {elapsed:.1f}s")
    print(f"    TPS: {tps:.1f}")
    print(f"    P99: {p99:.0f}ms")


# ============================================================
# 校验阶段
# ============================================================
def refresh_balances(wallets: list[WalletInfo], headers: dict) -> list[WalletInfo]:
    """刷新钱包余额"""
    updated = []
    for w in wallets:
        resp = api_get(WALLET_PAGE_URL, {"walletType": "40", "userId": str(w.userId), "pageNo": 1, "pageSize": 1}, headers)
        items = resp.get("data", {}).get("list", [])
        if items:
            w.balance = items[0]["balance"]
            w.freezePrice = items[0].get("freezePrice", 0)
        updated.append(w)
    return updated


def verify(headers: dict, wallets_before: list[WalletInfo]):
    print("\n" + "=" * 60)
    print("校验阶段")
    print("=" * 60)

    wallets_after = refresh_balances(wallets_before, headers)

    errors = []
    for w in wallets_after:
        if w.balance < 0:
            errors.append(f"  ❌ {w.mobile}: 余额为负数 ({w.balance})")
    if errors:
        for e in errors:
            print(e)
        print(f"\n  ❌ 发现 {len(errors)} 个钱包余额异常")
    else:
        print("  ✅ 所有钱包余额 ≥ 0")

    # 流水校验（抽样前5个用户）
    print("\n  流水抽样校验:")
    for w in wallets_after[:5]:
        resp = api_get(TRANSACTION_PAGE_URL, {"userId": str(w.userId), "pageNo": 1, "pageSize": 5}, headers)
        total = resp.get("data", {}).get("total", 0)
        items = resp.get("data", {}).get("list", [])
        has_duplicate = len({t.get("id") for t in items}) != len(items)
        print(f"    {w.mobile}: 流水 {total} 条, 无重复: {'✅' if not has_duplicate else '❌'}")

    # 导出报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORT_DIR, f"verify_{timestamp}.csv")
    with open(report_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["mobile", "userId", "walletId", "balance", "freezePrice", "available"])
        for w in wallets_after:
            writer.writerow([w.mobile, w.userId, w.walletId, w.balance, w.freezePrice, w.available])
    print(f"\n  📄 余额报表: {report_path}")


# ============================================================
# 主入口
# ============================================================
def main():
    print("=" * 60)
    print("用户提现压测")
    print(f"环境: {ADMIN_URL}")
    print(f"模式: {'走网关' if USE_GATEWAY else f'直连实例 {PAY_INSTANCES}'}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 0) 获取 admin token
    print("\n[0/4] 管理员登录...")
    headers = build_admin_headers()

    # 1) 准备用户
    print("\n[1/4] 准备测试用户...")
    wallets = setup_users(headers)
    if not wallets:
        print("[ERROR] 没有可用的测试用户")
        return
    print(f"  共 {len(wallets)} 个用户可用")

    # 2) 场景一：防超扣
    print("\n[2/4] 开始压测场景...")
    scenario_anti_oversubtraction(headers, wallets)

    # 3) 场景二：吞吐量
    scenario_throughput(headers, wallets)

    # 4) 场景三：混合
    scenario_mixed(headers, wallets)

    # 5) 校验
    print("\n[3/4] 数据校验...")
    verify(headers, wallets)

    print(f"\n[4/4] 压测完成，报告目录: {REPORT_DIR}")


if __name__ == "__main__":
    main()
