import pytest
from config import ADMIN_URL


class TestPromotionCombinationActivityCreate:
    """创建拼团活动"""

    @pytest.mark.smoke
    def test_PromotionCombinationActivityCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/combination-activity/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
