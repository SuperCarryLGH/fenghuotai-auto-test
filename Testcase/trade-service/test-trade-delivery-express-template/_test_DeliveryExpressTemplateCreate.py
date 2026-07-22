import pytest
from config import ADMIN_URL


class TestDeliveryExpressTemplateCreate:
    """创建快递运费模板"""

    @pytest.mark.smoke
    def test_DeliveryExpressTemplateCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express-template/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
