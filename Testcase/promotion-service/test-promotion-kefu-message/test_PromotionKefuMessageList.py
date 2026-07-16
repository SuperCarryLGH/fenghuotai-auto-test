import pytest
from config import APP_URL


class TestPromotionKefuMessageList:
    """获得客服消息列表"""

    @pytest.mark.smoke
    def test_PromotionKefuMessageList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/kefu-message/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
