import pytest
from config import ADMIN_URL


class TestPromotionCouponTemplateDelete:
    """删除优惠劵模板"""

    @pytest.mark.smoke
    def test_PromotionCouponTemplateDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/coupon-template/delete"
        params = {"id": "promotion_coupon_template_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
