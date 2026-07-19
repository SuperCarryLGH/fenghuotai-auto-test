import pytest
from config import APP_URL


class TestPromotionCouponTemplateList:
    """获得优惠劵模版列表"""

    @pytest.mark.smoke
    def test_PromotionCouponTemplateList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/coupon-template/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
