import pytest
from config import ADMIN_URL


class TestSystemNoticeGet:
    """获得通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeGet(self, api_session, auth_headers, autotest_notice_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/notice/get"
        params = {"id": autotest_notice_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
