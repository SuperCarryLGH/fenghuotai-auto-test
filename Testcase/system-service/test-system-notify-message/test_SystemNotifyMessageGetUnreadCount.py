import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageGetUnreadCount:
    """获得当前用户的未读站内信数量"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageGetUnreadCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/get-unread-count"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
