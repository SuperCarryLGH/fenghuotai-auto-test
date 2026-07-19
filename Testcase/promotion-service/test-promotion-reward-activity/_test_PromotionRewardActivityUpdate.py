import pytest
from config import ADMIN_URL


class TestPromotionRewardActivityUpdate:
    """更新满减送活动"""

    @pytest.mark.smoke
    def test_PromotionRewardActivityUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/reward-activity/update"
        body = {"id": "promotion_reward_activity_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
