import pytest
from config import APP_URL


class TestPromotionBargainRecordGetDetail:
    """获得砍价记录的明细"""

    @pytest.mark.smoke
    def test_PromotionBargainRecordGetDetail(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/bargain-record/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
