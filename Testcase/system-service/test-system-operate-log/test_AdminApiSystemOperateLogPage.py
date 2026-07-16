import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiSystemOperateLogPage:
    """查看操作日志分页列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemOperateLogPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/operate-log/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize']
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
