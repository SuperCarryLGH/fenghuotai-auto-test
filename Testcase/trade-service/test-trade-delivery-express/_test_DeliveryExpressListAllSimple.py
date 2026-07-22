import pytest
from config import ADMIN_URL


class TestDeliveryExpressListAllSimple:
    """获取快递公司精简信息列表"""

    @pytest.mark.smoke
    def test_DeliveryExpressListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
