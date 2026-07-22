import pytest
from config import APP_URL


class TestPromotionPointActivityPage:
    """获得积分商城活动分页"""

    @pytest.mark.smoke
    def test_PromotionPointActivityPage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/point-activity/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
