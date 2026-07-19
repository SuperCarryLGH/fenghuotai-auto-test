import pytest
from config import APP_URL


class TestPromotionDiyPageGet:
    """获得装修页面"""

    @pytest.mark.smoke
    def test_PromotionDiyPageGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/diy-page/get"
        params = {"id": "promotion_diy_page_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
