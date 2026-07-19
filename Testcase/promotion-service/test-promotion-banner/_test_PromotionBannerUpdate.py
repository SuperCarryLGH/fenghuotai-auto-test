import pytest
from config import ADMIN_URL


class TestPromotionBannerUpdate:
    """更新 Banner"""

    @pytest.mark.smoke
    def test_PromotionBannerUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/banner/update"
        body = {"id": "promotion_banner_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
