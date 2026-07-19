import pytest
from config import ADMIN_URL


class TestAfterSaleRefuse:
    """拒绝收货"""

    @pytest.mark.smoke
    def test_AfterSaleRefuse(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/after-sale/refuse"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
