import pytest
from config import ADMIN_URL


class TestPromotionKefuConversationList:
    """获得客服会话列表"""

    @pytest.mark.smoke
    def test_PromotionKefuConversationList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/kefu-conversation/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
