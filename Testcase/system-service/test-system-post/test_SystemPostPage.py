import pytest
from config import ADMIN_URL


class TestSystemPostPage:
    """获得岗位分页列表"""

    @pytest.mark.smoke
    def test_SystemPostPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
