import pytest
from config import ADMIN_URL


class TestDeliveryPickUpStoreCreate:
    """创建自提门店"""

    @pytest.mark.smoke
    def test_DeliveryPickUpStoreCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/pick-up-store/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
