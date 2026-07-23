import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuCreate:
    """创建菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuCreate(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/create"
        params = {
            "id":1212,
            "name": menu["menu"]["name"],
            "parentId": menu["menu"]["parentId"],
            "type": menu["menu"]["type"],
            "sort": 0,
            "status": menu["menu"]["status"]
            }

        ok(api_session.post(url, headers=auth_headers,json=params))
        assert data["msg"] == "父菜单的类型必须是目录或者菜单"
        print(data)
