import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


@pytest.mark.skip(reason="接口参数待确认")
class Test_AdminApiFenceUpdate:
    """admin更新电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "fenceName": f"更新围栏_{suffix}",
            "fenceLevel": 1,
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
