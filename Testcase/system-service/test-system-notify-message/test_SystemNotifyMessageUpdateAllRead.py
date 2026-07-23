import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageUpdateAllRead:
    """标记所有站内信为已读"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageUpdateAllRead(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/update-all-read"
        body = {"id": 1}  # TODO: 补充参数
        ok(api_session.put(url, json=body, headers=auth_headers))
