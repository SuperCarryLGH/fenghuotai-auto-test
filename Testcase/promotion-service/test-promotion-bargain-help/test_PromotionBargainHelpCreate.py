import pytest
from config import APP_URL


class TestPromotionBargainHelpCreate:
    """创建砍价助力"""

    @pytest.mark.smoke
    def test_PromotionBargainHelpCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/bargain-help/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
