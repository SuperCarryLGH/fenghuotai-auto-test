import pytest
from config import ADMIN_URL


class TestDeliveryExpressCreate:
    """创建快递公司"""

    @pytest.mark.smoke
    def test_DeliveryExpressCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express/create"
        body = {"code": f"EXP_194199", "name": f"快递_194199", "sort": 0, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
