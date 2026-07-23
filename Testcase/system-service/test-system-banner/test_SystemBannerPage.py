import pytest
from config import ADMIN_URL


class TestSystemBannerPage:
    """获得 Banner 分页"""

    @pytest.mark.smoke
    def test_SystemBannerPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/banner/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
