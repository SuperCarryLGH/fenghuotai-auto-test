import pytest
from config import ADMIN_URL


class TestPayWalletPage:
    """获得钱包分页（按 walletType 区分持有人）"""

    @pytest.mark.smoke
    def test_PayWalletPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            "walletType": 40,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
