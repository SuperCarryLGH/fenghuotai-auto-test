import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageGetUnreadList:
    """获取当前用户的最新站内信列表，默认 10 条"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageGetUnreadList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/get-unread-list"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
