import pytest
from config import ADMIN_URL


class TestPromotionPointActivityDelete:
    """删除积分商城活动"""

    @pytest.mark.smoke
    def test_PromotionPointActivityDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/point-activity/delete"
        params = {"id": "promotion_point_activity_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
