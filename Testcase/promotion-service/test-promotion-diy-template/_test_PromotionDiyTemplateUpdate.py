import pytest
from config import ADMIN_URL


class TestPromotionDiyTemplateUpdate:
    """更新装修模板"""

    @pytest.mark.smoke
    def test_PromotionDiyTemplateUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-template/update"
        body = {"id": "promotion_diy_template_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
