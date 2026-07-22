import pytest
import time
from config import APP_URL
from Common.login import Login


class TestPayWalletTransactionGetSummary:
    """获得钱包流水统计"""

    @pytest.mark.smoke
    def test_PayWalletTransactionGetSummary(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/pay/wallet-transaction/get-summary"
        params = {}
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
