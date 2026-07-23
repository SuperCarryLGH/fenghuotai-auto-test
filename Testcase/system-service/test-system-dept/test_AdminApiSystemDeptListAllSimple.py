import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptListAllSimple:
    """获取部门精简信息列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptListAllSimple(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/list-all-simple"
        params = {
                   # "name": dept["dept"]["name"],
                   # "status": dept["dept"]["status"]
            }

        ok(api_session.get(url, headers=auth_headers,params=params,))