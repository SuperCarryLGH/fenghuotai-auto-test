import pytest
from config import ADMIN_URL


class TestSystemNoticeDeleteList:
    """批量删除通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeDeleteList(self, api_session, auth_headers, system_notice_id):
        url = f"{ADMIN_URL}/admin-api/system/notice/delete-list"
        params = {"ids": str(autotest_notice_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
