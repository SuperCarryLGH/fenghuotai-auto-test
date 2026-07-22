import pytest
from config import ADMIN_URL


class TestOrderPickUpByVerifyCode:
    """订单核销"""

    @pytest.mark.smoke
    def test_OrderPickUpByVerifyCode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/order/pick-up-by-verify-code"
        body = {"verifyCode": "9999"}  # TODO: 使用实际核销码
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
