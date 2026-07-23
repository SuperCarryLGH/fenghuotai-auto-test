import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageGetUnreadList:
    """获取当前用户的最新站内信列表，默认 10 条"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageGetUnreadList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/get-unread-list"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=auth_headers))
