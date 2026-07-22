import pytest
from config import APP_URL


class TestOrderCreate:
    """创建订单"""

    @pytest.mark.smoke
    def test_OrderCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
