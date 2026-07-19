import pytest
from config import ADMIN_URL


class TestDeliveryPickUpStoreBind:
    """绑定自提店员"""

    @pytest.mark.smoke
    def test_DeliveryPickUpStoreBind(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/pick-up-store/bind"
        body = {"id": "trade_delivery_pick_up_store_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
