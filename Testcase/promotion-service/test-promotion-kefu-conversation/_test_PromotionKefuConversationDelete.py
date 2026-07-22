import pytest
from config import ADMIN_URL


class TestPromotionKefuConversationDelete:
    """删除客服会话"""

    @pytest.mark.smoke
    def test_PromotionKefuConversationDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/kefu-conversation/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
