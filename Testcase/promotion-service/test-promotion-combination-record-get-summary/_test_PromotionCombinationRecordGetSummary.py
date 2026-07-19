import pytest
from config import APP_URL


class TestPromotionCombinationRecordGetSummary:
    """获得拼团记录的概要信息"""

    @pytest.mark.smoke
    def test_PromotionCombinationRecordGetSummary(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/combination-record/get-summary"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
