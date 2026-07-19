import pytest
from config import ADMIN_URL


class TestDeliveryPickUpStoreSimpleList:
    """获得自提门店精简信息列表"""

    @pytest.mark.smoke
    def test_DeliveryPickUpStoreSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/pick-up-store/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
