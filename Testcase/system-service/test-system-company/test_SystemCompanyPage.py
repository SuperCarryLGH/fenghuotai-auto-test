import pytest
from config import ADMIN_URL


class TestSystemCompanyPage:
    """获得公司分页"""

    @pytest.mark.smoke
    def test_SystemCompanyPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/company/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
