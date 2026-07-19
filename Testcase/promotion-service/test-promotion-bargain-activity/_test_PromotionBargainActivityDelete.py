import pytest
from config import ADMIN_URL


class TestPromotionBargainActivityDelete:
    """删除砍价活动"""

    @pytest.mark.smoke
    def test_PromotionBargainActivityDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/bargain-activity/delete"
        params = {"id": "promotion_bargain_activity_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
