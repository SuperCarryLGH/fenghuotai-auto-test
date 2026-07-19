import pytest
from config import APP_URL


class TestPromotionCouponTemplateListByIds:
    """获得优惠劵模版列表"""

    @pytest.mark.smoke
    def test_PromotionCouponTemplateListByIds(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/coupon-template/list-by-ids"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
