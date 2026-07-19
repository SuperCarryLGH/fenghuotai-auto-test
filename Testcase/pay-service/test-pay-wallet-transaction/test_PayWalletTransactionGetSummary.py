import pytest
from config import APP_URL


class TestPayWalletTransactionGetSummary:
    """获得钱包流水统计"""

    @pytest.mark.smoke
    def test_PayWalletTransactionGetSummary(self, api_session, station_token):
        url = f"{APP_URL}/app-api/pay/wallet-transaction/get-summary"
        params = {}
        resp = api_session.get(url, params=params, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
