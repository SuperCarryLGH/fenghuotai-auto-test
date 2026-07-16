import pytest
from config import APP_URL


class TestPayWalletRechargePage:
    """获得钱包充值记录分页"""

    @pytest.mark.smoke
    def test_PayWalletRechargePage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/pay/wallet-recharge/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
