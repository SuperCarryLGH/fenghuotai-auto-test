import pytest
from config import ADMIN_URL


class TestPromotionCouponDelete:
    """回收优惠劵"""

    @pytest.mark.smoke
    def test_PromotionCouponDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/coupon/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
