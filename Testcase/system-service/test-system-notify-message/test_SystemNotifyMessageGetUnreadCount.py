import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageGetUnreadCount:
    """获得当前用户的未读站内信数量"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageGetUnreadCount(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/get-unread-count"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=auth_headers))
