import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_banner

common = load_common()
banner_data = load_system_banner()


class Test_AdminApiSystemBannerCreate:
    """admin创建Banner"""

    @pytest.mark.smoke
    def test_AdminApiSystemBannerCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/banner/create"
        suffix = str(int(time.time()))
        body = {
            "title": f"{banner_data['banner']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
