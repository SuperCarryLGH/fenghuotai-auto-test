import pytest
from config import ADMIN_URL


class TestPromotionPointActivityUpdate:
    """更新积分商城活动"""

    @pytest.mark.smoke
    def test_PromotionPointActivityUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/point-activity/update"
        body = {"id": "promotion_point_activity_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
