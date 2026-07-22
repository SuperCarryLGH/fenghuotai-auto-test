import pytest
from config import ADMIN_URL


class TestAfterSaleDisagree:
    """拒绝售后"""

    @pytest.mark.smoke
    def test_AfterSaleDisagree(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/after-sale/disagree"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
