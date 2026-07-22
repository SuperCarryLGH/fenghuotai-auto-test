import pytest
from config import APP_URL


class TestPromotionDiyTemplateGet:
    """获得装修模板"""

    @pytest.mark.smoke
    def test_PromotionDiyTemplateGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/diy-template/get"
        params = {"id": "promotion_diy_template_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
