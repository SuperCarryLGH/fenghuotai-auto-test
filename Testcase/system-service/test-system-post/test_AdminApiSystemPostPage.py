import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemPostPage:
    """获得岗位分页列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemPostPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
