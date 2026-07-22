import pytest
from config import ADMIN_URL


class TestDeliveryExpressTemplateList:
    """获得快递运费模板列表"""

    @pytest.mark.smoke
    def test_DeliveryExpressTemplateList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express-template/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
