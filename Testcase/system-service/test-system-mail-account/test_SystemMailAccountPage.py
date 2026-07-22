import pytest
from config import ADMIN_URL


class TestSystemMailAccountPage:
    """获得邮箱账号分页"""

    @pytest.mark.smoke
    def test_SystemMailAccountPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
