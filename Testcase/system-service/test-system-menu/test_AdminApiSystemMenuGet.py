import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuGet:
    """获取菜单信息"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/get"
        params = {
            "id": 100
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        print(data)
