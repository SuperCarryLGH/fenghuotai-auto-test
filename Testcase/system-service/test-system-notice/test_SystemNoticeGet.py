import pytest
from config import ADMIN_URL


class TestSystemNoticeGet:
    """获得通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notice/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
