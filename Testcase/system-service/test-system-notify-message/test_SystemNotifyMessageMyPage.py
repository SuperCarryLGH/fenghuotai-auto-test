import pytest
from config import ADMIN_URL


class TestSystemNotifyMessageMyPage:
    """获得我的站内信分页"""

    @pytest.mark.smoke
    def test_SystemNotifyMessageMyPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notify-message/my-page"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
