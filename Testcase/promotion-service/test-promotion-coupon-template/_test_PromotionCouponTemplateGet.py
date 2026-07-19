import pytest
from config import APP_URL


class TestPromotionCouponTemplateGet:
    """获得优惠劵模版"""

    @pytest.mark.smoke
    def test_PromotionCouponTemplateGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/coupon-template/get"
        params = {"id": "promotion_coupon_template_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
