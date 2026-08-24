import pytest
from config import APP_URL
from Common.login import Login


class TestPayWalletAppPage:
    @pytest.mark.smoke
    def test_PayWalletAppPage(self,api_session,login_tool):
        token = login_tool.app_login(mobile="15617600003")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/pay/wallet-transaction/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, json=params, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        print(data)