import pytest
from config import ADMIN_URL


class TestSystemNotifyMessagePage:
    """获得站内信分页"""

    @pytest.mark.smoke
    def test_SystemNotifyMessagePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
