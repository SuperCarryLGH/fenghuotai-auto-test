import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageUpdateRead:
    """标记站内信为已读"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageUpdateRead(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/update-read"
        params = {"ids": [1]}
        ok(api_session.put(url, params=params, headers=auth_headers))
