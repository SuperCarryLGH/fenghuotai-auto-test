import pytest
from config import APP_URL


class TestPromotionPointActivityListByIds:
    """获得积分商城活动列表，基于活动编号数组"""

    @pytest.mark.smoke
    def test_PromotionPointActivityListByIds(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/point-activity/list-by-ids"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
