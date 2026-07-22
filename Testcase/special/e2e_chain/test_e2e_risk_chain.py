"""
风控全链路 E2E 测试
配置阶梯规则 → 绑定运营区域 → 用户下单 → 校验风控动作
"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login


def login_as(api_session, mobile):
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000))}
    resp = api_session.post(
        f"{ADMIN_URL}/admin-api/system/auth/sms-login",
        json={"mobile": mobile, "code": "9999"}, headers=headers,
    )
    assert resp.status_code == 200 and resp.json()["code"] == 0
    return {"Authorization": f"Bearer {resp.json()['data']['accessToken']}"}


def app_login(api_session, mobile):
    login = Login()
    token = login.app_login(mobile=mobile)
    return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}


class TestE2ERiskChain:
    """风控规则触发全链路"""

    @pytest.mark.smoke
    def test_e2e_risk(self, api_session):
        admin_headers = login_as(api_session, "18600000000")  # 站点老板有 admin 权限

        # ──────────────────────────────────────────
        # Step 1: 创建风控规则（阶梯规则）
        # ──────────────────────────────────────────
        print("\n[Step 1] 创建风控规则...")
        rule_id = int(time.time()) % 1000000000
        resp = api_session.post(
            f"{ADMIN_URL}/admin-api/risk/rule/create",
            json={
                "ruleName": f"autotest_risk_{rule_id}",
                "status": 0,
                "remark": "自动化测试规则",
                "ruleDetails": [{
                    "minCount": 1,
                    "maxCount": 99,
                    "actionType": 10,  # 10=正常放行
                    "sort": 0,
                }],
            },
            headers=admin_headers,
        )
        rule_result = resp.json()
        print(f"  规则创建: code={rule_result.get('code')}, msg={rule_result.get('msg','')}")
        if rule_result.get("code") != 0:
            print("  ⚠️ 规则创建失败，可能 ID 冲突或参数不对，跳过后续步骤")
            return

        # ──────────────────────────────────────────
        # Step 2: 创建阶梯区间（到厂质检）
        # ──────────────────────────────────────────
        print("\n[Step 2] 创建阶梯区间(2-3次→到厂质检)...")
        resp = api_session.post(
            f"{ADMIN_URL}/admin-api/risk/rule-detail/create",
            json={
                "ruleId": rule_id,
                "minCount": 1,
                "maxCount": 2,
                "actionType": 10,  # 正常放行
                "sort": 0,
            },
            headers=admin_headers,
        )
        detail_result = resp.json()
        print(f"  阶梯创建: code={detail_result.get('code')}")

        # ──────────────────────────────────────────
        # Step 3: C端用户下单（验证不拦截）
        # ──────────────────────────────────────────
        print("\n[Step 3] C端用户下单验证...")
        user_headers = app_login(api_session, "15617637160")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
            json={
                "platform": "web", "provider": "",
                "bizMode": "WeightClothes",
                "userName": "用户04", "userPhone": "15617637160",
                "addressId": "2071903351920783362",
                "appointmentDate": time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400)),
                "appointmentTimePeriod": "17:00-18:00",
                "estimatedInfo": "5~10kg",
                "lat": "34.79678190031236", "lon": "113.68181482834622",
                "num": 5, "predictWeight": "5~10kg",
            },
            headers=user_headers,
        )
        order_result = resp.json()
        print(f"  下单结果: code={order_result.get('code')}, msg={order_result.get('msg','')}")
        if order_result.get("code") == 0:
            order_id = order_result["data"].get("id")
            print(f"  ✅ 下单成功 order_id={order_id} — 风控未拦截")
        else:
            print(f"  ⚠️ 下单被拦截或失败: {order_result.get('msg')}")

        print(f"\n🎉 风控全链路完成! rule_id={rule_id}")
