import pytest
from config import ADMIN_URL


class TestDeliveryExpressTemplateUpdate:
    """更新快递运费模板"""

    @pytest.mark.smoke
    def test_DeliveryExpressTemplateUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express-template/update"
        body = {"id": autotest_express_template_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
