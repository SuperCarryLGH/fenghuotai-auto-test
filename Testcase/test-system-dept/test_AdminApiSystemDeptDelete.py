import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptDelete:
    """admin删除部门"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptDelete(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/delete"
        params = {
            "id": dept["dept"]["create id"],
            }

        resp = api_session.delete(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 1002004002
        print(data)