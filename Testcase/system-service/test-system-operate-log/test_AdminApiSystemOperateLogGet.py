import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiSystemOperateLogGet:
    """查看操作日志"""

    @pytest.mark.smoke
    def test_AdminApiSystemOperateLogGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/operate-log/get"
        params = {
            "id" : 1024
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
