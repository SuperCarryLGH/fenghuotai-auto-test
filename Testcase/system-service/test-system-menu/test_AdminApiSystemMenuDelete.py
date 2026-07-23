import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuDelete:
    """删除菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuDelete(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/delete"
        params = {
            "id": 1213
            }

        ok(api_session.delete(url, headers=auth_headers,params=params))
        data = resp.json()
        #assert data["code"] == 0
        print(data)
