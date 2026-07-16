import pytest
from config import ADMIN_URL


class TestPayWalletPageStation:
    """获得站点钱包流水分页"""

    @pytest.mark.smoke
    def test_PayWalletPageStation(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/page-station"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
