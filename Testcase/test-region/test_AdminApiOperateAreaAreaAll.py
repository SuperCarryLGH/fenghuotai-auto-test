import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaAreaAll:
    """admin获取全部分区"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaAreaAll(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/area-all"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
