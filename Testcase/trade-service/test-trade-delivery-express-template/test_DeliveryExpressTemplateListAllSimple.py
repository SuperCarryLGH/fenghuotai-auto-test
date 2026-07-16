import pytest
from config import ADMIN_URL


class TestDeliveryExpressTemplateListAllSimple:
    """获取快递模版精简信息列表"""

    @pytest.mark.smoke
    def test_DeliveryExpressTemplateListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express-template/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
