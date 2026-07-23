import pytest
from config import ADMIN_URL


class TestSystemOperateAreaBizOpenStatus:
    """更新业务开通状态"""

    @pytest.mark.smoke
    def test_SystemOperateAreaBizOpenStatus(self, api_session, auth_headers, autotest_operate_area_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/biz-open-status"
        params = {"ids": [autotest_operate_area_id], "status": 1}
        ok(api_session.put(url, params=params, headers=auth_headers))
