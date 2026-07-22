import pytest
from config import APP_URL


class TestPromotionCombinationRecordGetHeadList:
    """获得最近 n 条拼团记录（团长发起的）"""

    @pytest.mark.smoke
    def test_PromotionCombinationRecordGetHeadList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/combination-record/get-head-list"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
