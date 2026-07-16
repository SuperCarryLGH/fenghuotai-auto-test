import pytest
from config import APP_URL


class TestPromotionCouponTake:
    """领取优惠劵"""

    @pytest.mark.smoke
    def test_PromotionCouponTake(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/coupon/take"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
