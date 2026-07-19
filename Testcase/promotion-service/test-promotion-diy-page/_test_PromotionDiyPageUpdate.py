import pytest
from config import ADMIN_URL


class TestPromotionDiyPageUpdate:
    """更新装修页面"""

    @pytest.mark.smoke
    def test_PromotionDiyPageUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-page/update"
        body = {"id": "promotion_diy_page_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
