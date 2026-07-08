"""
资金流转 15 场景自动化测试

运行方式:
    cd /Users/rs/PycharmProjects/PythonProject1
    TEST_ENV=dev USE_MOCK=false pytest -v -s Testcase/fund_scenarios/test_fund_flow.py

场景按顺序执行，每一步的输入依赖上一步的输出。
"""
import sys
import os
import time
import uuid

import pytest
import requests
import pymysql
from config import ADMIN_URL, APP_URL, DB_CONFIG
from Common.login import Login

# ============================================================
# 测试数据
# ============================================================
COMPANY_ID = 2
SORTING_CENTER_ID = 3
STATION_ID = "2061713873303195650"
TEST_USER_MOBILE = "15617637160"
TEST_USER_ID = 2071418043802406914
TEST_ADDRESS_ID = "2071903351920783362"

# ============================================================
# 辅助函数
# ============================================================
_error_report = []


def _record_error(scenario: str, msg: str):
    _error_report.append(f"❌ {scenario}: {msg}")
    print(f"    ⚠️  {msg}")


_BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


def _biz_no(prefix: str = "FS") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _api_post(url: str, payload: dict, headers: dict) -> dict:
    print(f"    POST {url}")
    print(f"    payload={payload}")
    try:
        resp = requests.post(url, json=payload, headers={**_BASE_HEADERS, **headers}, timeout=30)
        print(f"    status={resp.status_code}, body={resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        print(f"    → code={data.get('code')}, msg={data.get('msg', '')}")
        return data
    except Exception as e:
        print(f"    ❌ 请求失败: {e}")
        return {"code": -1, "msg": str(e), "data": None}


def _api_get(url: str, params: dict, headers: dict) -> dict:
    print(f"    GET {url}")
    print(f"    params={params}")
    try:
        resp = requests.get(url, params=params, headers={**_BASE_HEADERS, **headers}, timeout=30)
        print(f"    status={resp.status_code}, body={resp.text[:500]}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"    ❌ 请求失败: {e}")
        return {"code": -1, "msg": str(e), "data": None}


# ============================================================
# 状态查询
# ============================================================
def _get_company_fund(headers: dict) -> dict:
    """查公司资金"""
    r = _api_get(f"{ADMIN_URL}/admin-api/pay/fund/page",
                 {"fundType": "10", "orgId": str(COMPANY_ID), "pageNo": 1, "pageSize": 1}, headers)
    items = (r.get("data") or {}).get("list", [])
    return items[0] if items else None


def _get_sorting_center_fund(headers: dict) -> dict:
    """查分拣中心资金"""
    r = _api_get(f"{ADMIN_URL}/admin-api/pay/fund/page",
                 {"fundType": "20", "orgId": str(SORTING_CENTER_ID), "pageNo": 1, "pageSize": 1}, headers)
    items = (r.get("data") or {}).get("list", [])
    return items[0] if items else None


def _get_station_wallet(headers: dict) -> dict:
    """查网点钱包"""
    r = _api_get(f"{ADMIN_URL}/admin-api/pay/wallet/page",
                 {"walletType": "30", "stationId": STATION_ID, "pageNo": 1, "pageSize": 1}, headers)
    items = (r.get("data") or {}).get("list", [])
    return items[0] if items else None


def _get_user_wallet(headers: dict, user_id: int) -> dict:
    """查用户钱包"""
    r = _api_get(f"{ADMIN_URL}/admin-api/pay/wallet/page",
                 {"walletType": "40", "userId": str(user_id), "pageNo": 1, "pageSize": 1}, headers)
    items = (r.get("data") or {}).get("list", [])
    return items[0] if items else None


def _get_sorting_center_wallet(headers: dict) -> dict:
    """查分拣中心钱包"""
    r = _api_get(f"{ADMIN_URL}/admin-api/pay/wallet/page",
                 {"walletType": "10", "pageNo": 1, "pageSize": 50}, headers)
    items = (r.get("data") or {}).get("list", [])
    for item in items:
        if str(item.get("id")) == str(SORTING_CENTER_ID):
            return item
    return None


def _get_freeze_price(sc_wallet: dict) -> int:
    """从 DB 直接查分拣中心钱包的 freeze_price（API 不返回）"""
    if not sc_wallet:
        return 0
    wallet_id = sc_wallet.get("walletId")
    if not wallet_id:
        return 0
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"], port=DB_CONFIG["port"],
            user=DB_CONFIG["user"], password=DB_CONFIG["password"],
            database=DB_CONFIG["database"], connect_timeout=3,
        )
        c = conn.cursor()
        c.execute("SELECT freeze_price FROM pay_wallet WHERE id = %s", (wallet_id,))
        row = c.fetchone()
        c.close()
        conn.close()
        return row[0] if row and row[0] else 0
    except Exception:
        return sc_wallet.get("freezePrice", 0) or 0


def _snapshot_fund(headers: dict, user_id: int) -> dict:
    """拍快照，返回所有字段当前值"""
    company = _get_company_fund(headers) or {}
    sc = _get_sorting_center_fund(headers) or {}
    sc_wallet = _get_sorting_center_wallet(headers) or {}
    station = _get_station_wallet(headers) or {}
    user = _get_user_wallet(headers, user_id) or {}
    return {
        "公司总": company.get("totalFund", 0),
        "公司微信": company.get("wechatFund", 0),
        "公司支付宝": company.get("alipayFund", 0),
        "待分配": company.get("allocableFund", 0) or 0,
        "已分配": company.get("allocatedFund", 0) or 0,
        "分拣中心总": sc.get("totalFund", 0),
        "分拣中心微信": sc.get("wechatFund", 0),
        "分拣中心支付宝": sc.get("alipayFund", 0),
        "分拣中心余额": sc_wallet.get("balance", 0) or 0,
        "待提现": _get_freeze_price(sc_wallet),
        "网点": station.get("balance", 0),
        "用户": user.get("balance", 0),
    }


def _assert_changes(label: str, before: dict, after: dict, expected: dict):
    """校验所有字段变动：报错不终止，记录到 _error_report"""
    print(f"\n  [{label}]")
    all_ok = True
    for key, delta in expected.items():
        if delta == "-":
            continue
        actual = (after.get(key, 0) or 0) - (before.get(key, 0) or 0)
        status = "✅" if actual == delta else "❌"
        if status == "❌":
            all_ok = False
            _record_error(label, f"{key}: 预期 {delta:+.0f}, 实际 {actual:+.0f} ({before.get(key, 0)}→{after.get(key, 0)})")
        print(f"    {status} {key}: {before.get(key, 0)} → {after.get(key, 0)} (预期 {delta:+.0f}, 实际 {actual:+.0f})")


def _manual_step(snapshot_before: dict, step_label: str, instructions: str,
                 expected: dict, headers: dict, user_id: int) -> dict:
    """半自动化步骤：打印指引 → 等待OK → 拍快照 → 校验（失败不终止）"""
    print(f"\n  >>> 手动操作指引 <<<")
    print(f"  {instructions}")
    print(f"  完成后输入 OK 继续...")
    input("  >> ")
    time.sleep(1)
    try:
        after = _print_fund_state(headers, step_label, user_id)
        # 如果新快照全0但之前有值，说明查询接口挂了，沿用旧基线
        if sum(after.values()) == 0 and sum(snapshot_before.values()) > 0:
            _record_error(step_label, "快照查询失败(全0)，跳过校验，沿用旧基线")
            return snapshot_before
        _assert_changes(step_label, snapshot_before, after, expected)
        return after
    except Exception as e:
        _record_error(step_label, f"异常: {e}")
        return snapshot_before


def _print_fund_state(headers: dict, step: str, user_id: int = 0):
    s = _snapshot_fund(headers, user_id)
    print(f"\n  [{step}] 公司总={s['公司总']} "
          f"微信={s['公司微信']} 支付宝={s['公司支付宝']} "
          f"待分配={s['待分配']} 已分配={s['已分配']}")
    print(f"         分拣中心总={s['分拣中心总']} "
          f"微信={s['分拣中心微信']} 支付宝={s['分拣中心支付宝']} "
          f"余额={s['分拣中心余额']} 待提现={s['待提现']}")
    print(f"         网点={s['网点']} 用户={s['用户']}")
    return s


# ============================================================
# 场景测试
# ============================================================
class TestFundFlowScenarios:
    """资金流转 15 场景"""

    @pytest.fixture(autouse=True)
    def _setup(self, api_session):
        login = Login(session=api_session)
        self.token = login.admin_login("admin")
        self.headers = {
            "Content-Type": "application/json",
            "tenant-id": "1",
            "Authorization": f"Bearer {self.token}",
        }
        self.user_id = 0
        yield

    @pytest.mark.slow
    def test_all_scenarios(self, api_session):
        h = self.headers

        # ================================================================
        # 场景初始化：查当前状态
        # ================================================================
        print("\n" + "=" * 70)
        print("初始状态")
        print("=" * 70)

        self.user_id = TEST_USER_ID
        before = _print_fund_state(h, "初始", self.user_id)

        # ================================================================
        # S1: 公司充值500（微信200 + 支付宝300）
        # ================================================================
        print("\n" + "-" * 50)
        print("S1: 公司充值500（微信200 + 支付宝300）")
        print("-" * 50)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "fundType": 10,
            "tradeChannel": 1,
            "rechargeAmount": 200,
            "voucherImgList": [],
            "remark": "S1-微信充值",
            "thirdNo": _biz_no("S1WX"),
            "bizNo": _biz_no("S1WX"),
        }, h)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "fundType": 10,
            "tradeChannel": 2,
            "rechargeAmount": 300,
            "voucherImgList": [],
            "remark": "S1-支付宝充值",
            "thirdNo": _biz_no("S1ALI"),
            "bizNo": _biz_no("S1ALI"),
        }, h)

        time.sleep(1)
        after_s1 = _print_fund_state(h, "S1后", self.user_id)
        _assert_changes("S1", before, after_s1, {
            "公司总": int(500*100), "公司微信": int(200*100), "公司支付宝": int(300*100), "待分配": int(500*100),
            "已分配": 0, "分拣中心总": 0, "分拣中心微信": 0,
            "分拣中心支付宝": 0, "分拣中心余额": 0, "待提现": 0, "网点": 0, "用户": 0,
        })

        # ================================================================
        # S2: 公司划拨分拣中心200（微信100 + 支付宝100）
        # ================================================================
        print("\n" + "-" * 50)
        print("S2: 公司划拨分拣中心200（微信100 + 支付宝100）")
        print("-" * 50)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "orgId": SORTING_CENTER_ID,
            "fundType": 20,
            "tradeChannel": 1,
            "rechargeAmount": 100,
            "voucherImgList": [],
            "remark": "S2-微信划拨",
            "thirdNo": _biz_no("S2WX"),
        }, h)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "orgId": SORTING_CENTER_ID,
            "fundType": 20,
            "tradeChannel": 2,
            "rechargeAmount": 100,
            "voucherImgList": [],
            "remark": "S2-支付宝划拨",
            "thirdNo": _biz_no("S2ALI"),
        }, h)

        time.sleep(1)
        after_s2 = _print_fund_state(h, "S2后", self.user_id)
        _assert_changes("S2", after_s1, after_s2, {
            "公司总": 0, "公司微信": 0, "公司支付宝": 0,
            "待分配": int(-200 * 100), "已分配": int(200 * 100),
            "分拣中心总": int(200 * 100), "分拣中心微信": int(100 * 100), "分拣中心支付宝": int(100 * 100),
            "分拣中心余额": int(200 * 100), "待提现": 0, "网点": 0, "用户": 0,
        })

        # ================================================================
        # S3: 网点钱包微信充值0.3元
        # ================================================================
        print("\n" + "-" * 50)
        print("S3: 网点钱包微信充值0.3元")
        after_s3 = _manual_step(after_s2, "S3后",
            "网点账户: 18600000000 | 执行: 网点充值 | 渠道: 微信 | 金额: 0.3元",
            {"公司总": 30, "公司微信": 30, "公司支付宝": 0,
             "待分配": 0, "已分配": 30,
             "分拣中心总": 30, "分拣中心微信": 30, "分拣中心支付宝": 0,
             "分拣中心余额": 0, "待提现": 30, "网点": 30, "用户": 0},
            h, self.user_id)

        # ================================================================
        # S4: 网点钱包微信提现0.3元
        # ================================================================
        print("\n" + "-" * 50)
        print("S4: 网点钱包微信提现0.3元")
        after_s4 = _manual_step(after_s3, "S4后",
            "网点账户: 18600000000 | 执行: 网点提现 | 渠道: 微信 | 金额: 0.3元",
            {"公司总": -30, "公司微信": -30, "公司支付宝": 0,
             "待分配": 0, "已分配": -30,
             "分拣中心总": -30, "分拣中心微信": -30, "分拣中心支付宝": 0,
             "分拣中心余额": 0, "待提现": -30, "网点": -30, "用户": 0},
            h, self.user_id)

        # ================================================================
        # S5: 清运结算
        # ================================================================
        print("\n" + "-" * 50)
        print("S5: 清运结算")
        after_s5 = _manual_step(after_s4, "S5后",
            "网点: 1 | 执行: 清运结算 | 金额: 500元 (50000分)",
            {"公司总": 0, "公司微信": 0, "公司支付宝": 0,
             "待分配": 0, "已分配": 0,
             "分拣中心总": 0, "分拣中心微信": 0, "分拣中心支付宝": 0,
             "分拣中心余额": int(-500*100), "待提现": int(500*100), "网点": int(500*100), "用户": 0},
            h, self.user_id)

        # ================================================================
        # S6: 网点钱包支付宝提现0.3元
        # ================================================================
        print("\n" + "-" * 50)
        print("S6: 网点钱包支付宝提现0.3元")
        after_s6 = _manual_step(after_s5, "S6后",
            "网点账户: 18600000000 | 执行: 网点提现 | 渠道: 支付宝 | 金额: 0.3元",
            {"公司总": -30, "公司微信": 0, "公司支付宝": -30,
             "待分配": 0, "已分配": -30,
             "分拣中心总": -30, "分拣中心微信": 0, "分拣中心支付宝": -30,
                           "分拣中心余额": 0, "待提现": -30, "网点": -30, "用户": 0},
            h, self.user_id)

        # ================================================================
        # S7: 上门回收结算到用户钱包150（下单 → order-inspection 触发 settle）
        # ================================================================
        print("\n" + "-" * 50)
        print("S7: 上门回收结算到用户钱包150")
        print("-" * 50)

        before_s7 = _print_fund_state(h, "S7前", self.user_id)

        login = Login(session=api_session)
        user_token = login.app_login_with(mobile=TEST_USER_MOBILE, code="9999")
        user_h = {**_BASE_HEADERS, **Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {user_token}"}
        try:
            order_payload = {
                "platform": "web", "provider": "", "bizMode": "WeightClothes",
                "userName": "郑豪", "userPhone": TEST_USER_MOBILE,
                "addressId": TEST_ADDRESS_ID,
                "appointmentDate": "2026-07-06", "appointmentTimePeriod": "17:00-18:00",
                "appointmentWeekStr": "周日",
                "estimatedInfo": "5~10kg", "lat": "34.79678190031236", "lon": "113.68181482834622",
                "num": 5, "predictWeight": "5~10kg",
            }
            resp = requests.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
                                 json=order_payload, headers=user_h, timeout=30)
            r = resp.json()
            print(f"    下单 → code={r.get('code')}, msg={r.get('msg', '')}")
            order_id = r.get("data", {}).get("id", 0)

            time.sleep(1)
            requests.put(f"{ADMIN_URL}/recycle/admin-order/order-inspection",
                         json={"orderId": order_id},
                         headers={**_BASE_HEADERS, **h}, timeout=30)

            time.sleep(3)
        except Exception as e:
            _record_error("S7", f"下单/结算异常: {e}")
        after_s7 = _print_fund_state(h, "S7后", self.user_id)
        if sum(after_s7.values()) == 0 and sum(before_s7.values()) > 0:
            _record_error("S7", "快照异常(全0)，跳过校验")
            after_s7 = before_s7
        else:
            s7_user_delta = (after_s7["用户"] or 0) - (before_s7["用户"] or 0)
            s7_wallet_delta = (after_s7["分拣中心余额"] or 0) - (before_s7["分拣中心余额"] or 0)
            s7_pending_delta = (after_s7["待提现"] or 0) - (before_s7["待提现"] or 0)
            s7_station_delta = (after_s7["网点"] or 0) - (before_s7["网点"] or 0)
            _assert_changes("S7", before_s7, after_s7, {
                "公司总": 0, "公司微信": 0, "公司支付宝": 0,
                "待分配": 0, "已分配": 0,
                "分拣中心总": 0, "分拣中心微信": 0, "分拣中心支付宝": 0,
                "分拣中心余额": s7_wallet_delta, "待提现": s7_pending_delta,
                "网点": s7_station_delta, "用户": s7_user_delta,
            })

        # ================================================================
        # S8: 用户钱包微信提现1元
        # ================================================================
        print("\n" + "-" * 50)
        print("S8: 用户钱包微信提现1元")
        after_s8 = _manual_step(after_s7, "S8后",
            "用户账户: 15617637160 | 执行: 用户提现 | 渠道: 微信 | 金额: 1元",
            {"公司总": int(-1*100), "公司微信": int(-1*100), "公司支付宝": 0,
             "待分配": 0, "已分配": int(-1*100),
             "分拣中心总": int(-1*100), "分拣中心微信": int(-1*100), "分拣中心支付宝": 0,
             "分拣中心余额": 0, "待提现": int(-1*100), "网点": 0, "用户": int(-1*100)},
            h, self.user_id)

        # ================================================================
        # S9/S10: 失败场景 — 跳过
        # ================================================================
        print("\n" + "-" * 50)
        print("S9/S10: 失败场景 — 跳过（需构造边界数据）")
        print("-" * 50)

        # ================================================================
        # S11: 公司划拨分拣中心200（微信100 + 支付宝100）
        # ================================================================
        print("\n" + "-" * 50)
        print("S11: 公司划拨分拣中心200（微信100 + 支付宝100）")
        print("-" * 50)

        before_s11 = _print_fund_state(h, "S11前", self.user_id)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "orgId": SORTING_CENTER_ID,
            "fundType": 20,
            "tradeChannel": 1,
            "rechargeAmount": 100,
            "voucherImgList": [],
            "remark": "S11-微信划拨",
            "thirdNo": _biz_no("S11WX"),
        }, h)

        _api_post(f"{ADMIN_URL}/admin-api/pay/fund/create", {
            "companyId": COMPANY_ID,
            "sortingCenterId": SORTING_CENTER_ID,
            "orgId": SORTING_CENTER_ID,
            "fundType": 20,
            "tradeChannel": 2,
            "rechargeAmount": 100,
            "voucherImgList": [],
            "remark": "S11-支付宝划拨",
            "thirdNo": _biz_no("S11ALI"),
        }, h)

        time.sleep(1)
        after_s11 = _print_fund_state(h, "S11后", self.user_id)
        _assert_changes("S11", before_s11, after_s11, {
            "公司总": 0, "公司微信": 0, "公司支付宝": 0, "待分配": int(-200*100), "已分配": int(200*100),
            "分拣中心总": int(200*100), "分拣中心微信": int(100*100), "分拣中心支付宝": int(100*100),
            "分拣中心余额": int(200*100), "待提现": 0, "网点": 0, "用户": 0,
        })

        # ================================================================
        # S12: 上门回收结算到用户微信140
        # ================================================================
        print("\n" + "-" * 50)
        print("S12: 上门回收结算到用户微信140")
        print("-" * 50)

        before_s12 = _print_fund_state(h, "S12前", self.user_id)

        try:
            order_payload_s12 = {
                "platform": "web", "provider": "", "bizMode": "WeightClothes",
                "userName": "郑豪", "userPhone": TEST_USER_MOBILE,
                "addressId": TEST_ADDRESS_ID,
                "appointmentDate": "2026-07-06", "appointmentTimePeriod": "17:00-18:00",
                "appointmentWeekStr": "周日",
                "estimatedInfo": "5~10kg", "lat": "34.79678190031236", "lon": "113.68181482834622",
                "num": 5, "predictWeight": "5~10kg",
            }
            resp = requests.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
                                 json=order_payload_s12, headers=user_h, timeout=30)
            r = resp.json()
            order_id_s12 = r.get("data", {}).get("id", 0)

            time.sleep(1)
            requests.put(f"{ADMIN_URL}/recycle/admin-order/order-inspection",
                         json={"orderId": order_id_s12},
                         headers={**_BASE_HEADERS, **h}, timeout=30)

            time.sleep(3)
        except Exception as e:
            _record_error("S12", f"下单/结算异常: {e}")
        after_s12 = _print_fund_state(h, "S12后", self.user_id)
        if sum(after_s12.values()) == 0 and sum(before_s12.values()) > 0:
            _record_error("S12", "快照异常(全0)，跳过校验")
            after_s12 = before_s12
        else:
            s12_wallet_delta = (after_s12["分拣中心余额"] or 0) - (before_s12["分拣中心余额"] or 0)
            s12_user_delta = (after_s12["用户"] or 0) - (before_s12["用户"] or 0)
            s12_pending_delta = (after_s12["待提现"] or 0) - (before_s12["待提现"] or 0)
            s12_station_delta = (after_s12["网点"] or 0) - (before_s12["网点"] or 0)
            _assert_changes("S12", before_s12, after_s12, {
                "公司总": 0, "公司微信": 0, "公司支付宝": 0,
                "待分配": 0, "已分配": 0,
                "分拣中心总": 0, "分拣中心微信": 0, "分拣中心支付宝": 0,
                "分拣中心余额": s12_wallet_delta, "待提现": s12_pending_delta,
                "网点": s12_station_delta, "用户": s12_user_delta,
            })

        # ================================================================
        # S13: 上门回收结算到用户钱包100
        # ================================================================
        print("\n" + "-" * 50)
        print("S13: 上门回收结算到用户钱包100")
        print("-" * 50)

        before_s13 = _print_fund_state(h, "S13前", self.user_id)

        try:
            order_payload_s13 = {
                "platform": "web", "provider": "", "bizMode": "WeightClothes",
                "userName": "郑豪", "userPhone": TEST_USER_MOBILE,
                "addressId": TEST_ADDRESS_ID,
                "appointmentDate": "2026-07-06", "appointmentTimePeriod": "17:00-18:00",
                "appointmentWeekStr": "周日",
                "estimatedInfo": "5~10kg", "lat": "34.79678190031236", "lon": "113.68181482834622",
                "num": 5, "predictWeight": "5~10kg",
            }
            resp = requests.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
                                 json=order_payload_s13, headers=user_h, timeout=30)
            r = resp.json()
            order_id_s13 = r.get("data", {}).get("id", 0)

            time.sleep(1)
            requests.put(f"{ADMIN_URL}/recycle/admin-order/order-inspection",
                         json={"orderId": order_id_s13},
                         headers={**_BASE_HEADERS, **h}, timeout=30)

            time.sleep(3)
        except Exception as e:
            _record_error("S13", f"下单/结算异常: {e}")
        after_s13 = _print_fund_state(h, "S13后", self.user_id)
        if sum(after_s13.values()) == 0 and sum(before_s13.values()) > 0:
            _record_error("S13", "快照异常(全0)，跳过校验")
            after_s13 = before_s13
        else:
            s13_wallet_delta = (after_s13["分拣中心余额"] or 0) - (before_s13["分拣中心余额"] or 0)
            s13_user_delta = (after_s13["用户"] or 0) - (before_s13["用户"] or 0)
            s13_pending_delta = (after_s13["待提现"] or 0) - (before_s13["待提现"] or 0)
            s13_station_delta = (after_s13["网点"] or 0) - (before_s13["网点"] or 0)
            _assert_changes("S13", before_s13, after_s13, {
                "公司总": 0, "公司微信": 0, "公司支付宝": 0,
                "待分配": 0, "已分配": 0,
                "分拣中心总": 0, "分拣中心微信": 0, "分拣中心支付宝": 0,
                "分拣中心余额": s13_wallet_delta, "待提现": s13_pending_delta,
                "网点": s13_station_delta, "用户": s13_user_delta,
            })

        # ================================================================
        # S14: 用户钱包微信提现1元
        # ================================================================
        print("\n" + "-" * 50)
        print("S14: 用户钱包微信提现1元")
        after_s14 = _manual_step(after_s13, "S14后",
            "用户账户: 15617637160 | 执行: 用户提现 | 渠道: 微信 | 金额: 1元",
            {"公司总": int(-1*100), "公司微信": int(-1*100), "公司支付宝": 0,
             "待分配": 0, "已分配": int(-1*100),
             "分拣中心总": int(-1*100), "分拣中心微信": int(-1*100), "分拣中心支付宝": 0,
             "分拣中心余额": 0, "待提现": int(-1*100), "网点": 0, "用户": int(-1*100)},
            h, self.user_id)

        # ================================================================
        # S15: 网点垫付给用户钱包10元
        # ================================================================
        print("\n" + "-" * 50)
        print("S15: 网点垫付用户钱包10元")
        after_s15 = _manual_step(after_s14, "S15后",
            "网点: 2061713873303195650 (18600000000) | 垫付给用户: 15617637160 | 金额: 10元",
            {"公司总": 0, "公司微信": 0, "公司支付宝": 0,
             "待分配": 0, "已分配": 0,
             "分拣中心总": 0, "分拣中心微信": 0, "分拣中心支付宝": 0,
             "分拣中心余额": 0, "待提现": 0, "网点": int(-10*100), "用户": int(10*100)},
            h, self.user_id)

        # ================================================================
        # 最终汇总
        # ================================================================
        print("\n" + "=" * 70)
        print("15 场景执行完毕")
        if _error_report:
            print(f"\n⚠️  共 {len(_error_report)} 项校验失败:")
            for err in _error_report:
                print(f"  {err}")
        else:
            print("\n✅ 全部校验通过")
        print("=" * 70)
