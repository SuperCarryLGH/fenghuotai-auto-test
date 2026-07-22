import pytest
from config import ADMIN_URL


class TestPromotionDiyTemplateCreate:
    """创建装修模板"""

    @pytest.mark.smoke
    def test_PromotionDiyTemplateCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-template/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
