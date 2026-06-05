import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceUpdate:
    """admin更新电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/fence/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"更新围栏_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
