import pytest
from config import APP_URL


class TestPromotionRewardActivityGet:
    """获得满减送活动"""

    @pytest.mark.smoke
    def test_PromotionRewardActivityGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/reward-activity/get"
        params = {"id": "promotion_reward_activity_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
