import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaPage:
    """分页查询所有省份（一级）"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
