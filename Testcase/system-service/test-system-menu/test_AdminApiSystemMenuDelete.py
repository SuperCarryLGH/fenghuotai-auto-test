import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuDelete:
    """删除菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuDelete(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/delete"
        params = {
            "id": 1213
            }

        resp = api_session.delete(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        #assert data["code"] == 0
        print(data)
