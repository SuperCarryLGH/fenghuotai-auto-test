import pytest
from config import ADMIN_URL


class TestPromotionDiyPageCreate:
    """创建装修页面"""

    @pytest.mark.smoke
    def test_PromotionDiyPageCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-page/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
