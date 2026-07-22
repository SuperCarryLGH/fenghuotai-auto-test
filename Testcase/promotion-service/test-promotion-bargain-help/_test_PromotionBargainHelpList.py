import pytest
from config import APP_URL


class TestPromotionBargainHelpList:
    """获得砍价助力列表"""

    @pytest.mark.smoke
    def test_PromotionBargainHelpList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/bargain-help/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
