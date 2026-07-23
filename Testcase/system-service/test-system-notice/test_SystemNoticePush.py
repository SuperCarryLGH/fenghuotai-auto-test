import pytest
from config import ADMIN_URL


class TestSystemNoticePush:
    """推送通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticePush(self, api_session, auth_headers, autotest_notice_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/notice/push"
        params = {"id": autotest_notice_id}
        ok(api_session.post(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
