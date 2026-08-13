import pytest
from config import ADMIN_URL
from Common.loader import load_menu
menu = load_menu()

class Test_AdminApiSystemMenuCreate:
    """创建菜单"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/menu/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_AdminApiSystemMenuCreate(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/menu/create"
        params = {
            "id": 1212,
            "name": menu["menu"]["name"],
            "parentId": menu["menu"]["parentId"],
            "type": menu["menu"]["type"],
            "sort": 0,
            "status": menu["menu"]["status"]
            }

        resp = api_session.post(url, headers=auth_headers, json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["msg"] == "父菜单的类型必须是目录或者菜单"
        print(r)
