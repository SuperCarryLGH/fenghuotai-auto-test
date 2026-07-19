import pytest
from config import APP_URL


class TestPromotionBargainActivityGetDetail:
    """获得砍价活动详情"""

    @pytest.mark.smoke
    def test_PromotionBargainActivityGetDetail(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/bargain-activity/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
