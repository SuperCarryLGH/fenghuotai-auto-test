import pytest
from config import ADMIN_URL


class TestPayWalletTransactionPage:
    """获得钱包流水分页"""

    @pytest.mark.smoke
    def test_PayWalletTransactionPage(self, api_session, station_token):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
