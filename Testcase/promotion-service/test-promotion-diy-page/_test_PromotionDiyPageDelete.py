import pytest
from config import ADMIN_URL


class TestPromotionDiyPageDelete:
    """删除装修页面"""

    @pytest.mark.smoke
    def test_PromotionDiyPageDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-page/delete"
        params = {"id": "promotion_diy_page_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
