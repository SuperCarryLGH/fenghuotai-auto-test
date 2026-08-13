import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuDeleteList:
    """批量删除菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuDeleteList(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/delete-list"
        params = {
            "ids": [2147483647]
            }

        resp = api_session.delete(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        print(r)
