import pytest
from config import ADMIN_URL


class TestAfterSaleAgree:
    """同意售后"""

    @pytest.mark.smoke
    def test_AfterSaleAgree(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/after-sale/agree"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
