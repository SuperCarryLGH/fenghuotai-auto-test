import pytest
from config import APP_URL


class TestPromotionBannerList:
    """获得 banner 列表"""

    @pytest.mark.smoke
    def test_PromotionBannerList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/banner/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
