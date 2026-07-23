import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaFenceOpenStatus:
    """更新电子围栏开通状态"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaFenceOpenStatus(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/fence-open-status"
        params = {"ids": [common['common']['id']['valid']], "status": common['common']['status']['enabled']}
        ok(api_session.put(url, params=params, headers=auth_headers))
