import pytest
from config import ADMIN_URL


class TestDeliveryExpressTemplateGet:
    """获得快递运费模板"""

    @pytest.mark.smoke
    def test_DeliveryExpressTemplateGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express-template/get"
        params = {"id": "trade_delivery_express_template_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
