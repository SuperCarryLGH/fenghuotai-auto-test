import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageMyPage:
    """获得我的站内信分页"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageMyPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/my-page"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=auth_headers))
