import pytest
from config import ADMIN_URL


class TestPromotionCombinationActivityGet:
    """获得拼团活动"""

    @pytest.mark.smoke
    def test_PromotionCombinationActivityGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/combination-activity/get"
        params = {"id": "promotion_combination_activity_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
