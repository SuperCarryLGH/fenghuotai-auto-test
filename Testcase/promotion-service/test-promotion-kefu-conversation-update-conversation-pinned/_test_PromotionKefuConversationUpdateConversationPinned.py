import pytest
from config import ADMIN_URL


class TestPromotionKefuConversationUpdateConversationPinned:
    """置顶-取消置顶客服会话"""

    @pytest.mark.smoke
    def test_PromotionKefuConversationUpdateConversationPinned(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/kefu-conversation/update-conversation-pinned"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
