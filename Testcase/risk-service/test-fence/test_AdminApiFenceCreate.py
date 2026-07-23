import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceCreate:
    """admin创建电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/create"
        suffix = str(int(time.time()))
        body = {
            "fenceName": f"测试围栏_{suffix}",
            "fenceLevel": 1,
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.post(url, json=body, headers=auth_headers))
