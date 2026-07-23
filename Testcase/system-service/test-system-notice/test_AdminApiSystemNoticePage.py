import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemNoticePage:
    """获取通知公告列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemNoticePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notice/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
