import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceCreate:
    """admin创建电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/fence/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"测试围栏_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
