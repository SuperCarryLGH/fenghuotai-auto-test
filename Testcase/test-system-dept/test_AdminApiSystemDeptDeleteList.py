import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptDeleteList:
    """admin批量删除部门"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptDeleteList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/delete-list"
        params = {
            "ids": dept["dept"]["create id"],
            }

        resp = api_session.delete(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        print(data)