import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_page

common = load_common()
page = load_page()


class Test_AdminApiSystemUserPage:
    """获得用户分页列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/page"
        params = {
            "pageNo": page["page"]["pageNo"],
            "pageSize": page["page"]["pageSize"],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
