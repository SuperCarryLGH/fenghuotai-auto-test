import pytest
from config import APP_URL


class TestPromotionCombinationRecordGetDetail:
    """获得拼团记录明细"""

    @pytest.mark.smoke
    def test_PromotionCombinationRecordGetDetail(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/combination-record/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
