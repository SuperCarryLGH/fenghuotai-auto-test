import pytest
from config import APP_URL


class TestPromotionCouponGetUnusedCount:
    """获得未使用的优惠劵数量"""

    @pytest.mark.smoke
    def test_PromotionCouponGetUnusedCount(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/coupon/get-unused-count"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
