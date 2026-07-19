import pytest
from config import ADMIN_URL


class TestDeliveryPickUpStoreDelete:
    """删除自提门店"""

    @pytest.mark.smoke
    def test_DeliveryPickUpStoreDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/pick-up-store/delete"
        params = {"id": "trade_delivery_pick_up_store_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
