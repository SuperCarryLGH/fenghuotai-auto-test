import pytest
from config import ADMIN_URL


class TestSystemPostListAllSimple:
    """获取岗位全列表"""

    @pytest.mark.smoke
    def test_SystemPostListAllSimple(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/list-all-simple"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
