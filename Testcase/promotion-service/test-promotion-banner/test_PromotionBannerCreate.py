import pytest
from config import ADMIN_URL


class TestPromotionBannerCreate:
    """创建 Banner"""

    @pytest.mark.smoke
    def test_PromotionBannerCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/banner/create"
        body = {"title": f"测试Banner_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
