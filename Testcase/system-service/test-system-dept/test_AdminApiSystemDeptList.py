import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptList:
    """获取部门列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptList(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/list"
        params = {
                    "name": dept["dept"]["name"],
                    "status": dept["dept"]["status"]
            }

        ok(api_session.get(url, headers=auth_headers,params=params,))