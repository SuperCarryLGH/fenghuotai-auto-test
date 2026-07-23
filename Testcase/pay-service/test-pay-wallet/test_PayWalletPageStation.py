import time
import pytest
from config import ADMIN_URL, APP_URL
from Common.login import Login


class TestPayWalletPageStation:
    """获得站点钱包流水分页"""

    @pytest.mark.smoke
    def test_PayWalletPageStation(self, api_session, login_tool, ok):
        # ADMIN 端的 SMS 登录（不是 APP 端！）
        headers = {
            **Login.SMS_LOGIN_HEADERS,
            "timestamp": str(int(time.time() * 1000)),
        }
        ok(api_session.post(
            f"{ADMIN_URL}/admin-api/system/auth/sms-login",
            json={"mobile": "18600000000", "code": "9999"},
            headers=headers,
        ))
        token = resp.json()["data"]["accessToken"]

        url = f"{ADMIN_URL}/admin-api/pay/wallet/page-station"
        params = {"pageNo": 1, "pageSize": 10, "bizType": 11}
        resp2 = api_session.get(url, params=params, headers={"Authorization": f"Bearer {token}"})
        print(f"BODY: {resp2.text[:300]}")
        assert resp2.status_code == 200
        r = resp2.json()
        assert r["code"] == 0
        print(r)
