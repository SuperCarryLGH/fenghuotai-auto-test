import pytest
from config import ADMIN_URL


class TestOrderPickUpByVerifyCode:
    """订单核销"""

    @pytest.mark.smoke
    def test_OrderPickUpByVerifyCode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/order/pick-up-by-verify-code"
        params = {"pickUpVerifyCode": "9999"}
        resp = api_session.put(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
