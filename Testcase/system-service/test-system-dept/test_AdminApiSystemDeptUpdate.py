import pytest
from config import ADMIN_URL
from Common.loader import load_dept
dept = load_dept()

class Test_AdminApiSystemDeptUpdate:
    """更新部门"""

    @pytest.mark.smoke
    def test_AdminApiSystemDeptUpdate(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/dept/update"
        params = {
            "name": dept["dept"]["name"],
            "sort": dept["dept"]["sort"],
            "status": dept["dept"]["status"]
            }

        ok(api_session.put(url, headers=auth_headers,json=params))
        assert data["msg"] == "已经存在该名字的部门"
        print(data)