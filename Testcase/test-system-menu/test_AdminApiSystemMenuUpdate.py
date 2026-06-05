import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuUpdate:
    """admin修改菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuUpdate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/update"
        params = {
            "name": menu["menu"]["name"],
            "type": menu["menu"]["type"],
            "sort": menu["menu"]["sort"],
            "parent_id": menu["menu"]["parentId"],
            "status": menu["menu"]["status"]
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["msg"] == "请求参数不正确:父菜单 ID 不能为空"
        print(data)
