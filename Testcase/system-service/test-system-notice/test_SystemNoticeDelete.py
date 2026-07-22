import pytest
from config import ADMIN_URL


class TestSystemNoticeDelete:
    """删除通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeDelete(self, api_session, auth_headers, autotest_notice_id):
        url = f"{ADMIN_URL}/admin-api/system/notice/delete"
        params = {"id": autotest_notice_id}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
