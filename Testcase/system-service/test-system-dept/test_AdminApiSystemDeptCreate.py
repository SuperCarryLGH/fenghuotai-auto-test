import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptCreate:
    """创建部门"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptCreate(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/create"
        params = {
            "id": dept["dept"]["create id"],
            "name": dept["dept"]["create name"],
            "sort": 0,
            "status": dept["dept"]["status"]
            }

        ok(api_session.post(url, headers=auth_headers,json=params))
        #assert data["code"] == 0
        print(data)