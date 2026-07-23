import pytest
import time
from config import APP_URL
from Common.login import Login


class TestPayWalletRechargePage:
    """获得钱包充值记录分页"""

    @pytest.mark.smoke
    def test_PayWalletRechargePage(self, api_session, login_tool, ok):
        url = f"{APP_URL}/app-api/pay/wallet-recharge/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        ok(api_session.get(url, params=params, headers=headers))
