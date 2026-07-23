import pytest
from config import ADMIN_URL


class TestSystemOperateAreaFenceOpenStatus:
    """更新电子围栏开通状态"""

    @pytest.mark.smoke
    def test_SystemOperateAreaFenceOpenStatus(self, api_session, auth_headers, autotest_operate_area_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/fence-open-status"
        params = {"ids": [autotest_operate_area_id], "status": 1}
        ok(api_session.put(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
