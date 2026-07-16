import pytest
from config import ADMIN_URL


class TestPromotionCouponTemplateUpdateStatus:
    """更新优惠劵模板状态"""

    @pytest.mark.smoke
    def test_PromotionCouponTemplateUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/coupon-template/update-status"
        body = {"id": 1, "status": 0}  # TODO: 替换为实际 ID 和状态值
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
