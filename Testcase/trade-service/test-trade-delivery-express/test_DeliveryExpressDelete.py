import pytest
from config import ADMIN_URL


class TestDeliveryExpressDelete:
    """删除快递公司"""

    @pytest.mark.smoke
    def test_DeliveryExpressDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express/delete"
        params = {"id": autotest_express_id}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
