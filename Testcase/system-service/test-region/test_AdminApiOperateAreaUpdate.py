import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaUpdate:
    """更新系统-运营区域管理"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"更新运营区域_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
