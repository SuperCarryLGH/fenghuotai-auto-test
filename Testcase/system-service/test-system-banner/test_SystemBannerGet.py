import pytest
from config import ADMIN_URL


class TestSystemBannerGet:
    """获得 Banner"""

    @pytest.mark.smoke
    def test_SystemBannerGet(self, api_session, auth_headers, autotest_banner_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/banner/get"
        params = {"id": autotest_banner_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
