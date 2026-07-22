import pytest
from config import ADMIN_URL


class TestSystemNoticeUpdate:
    """修改通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeUpdate(self, api_session, auth_headers, autotest_notice_id):
        url = f"{ADMIN_URL}/admin-api/system/notice/update"
        body = {"id": autotest_notice_id, "title": "autotest_updated", "type": 1, "content": "autotest content", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
