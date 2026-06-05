import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaCreate:
    """admin创建运营区域"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"测试运营区域_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
