import pytest
from config import ADMIN_URL


class TestPromotionBannerGet:
    """获得 Banner"""

    @pytest.mark.smoke
    def test_PromotionBannerGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/banner/get"
        params = {"id": "promotion_banner_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
