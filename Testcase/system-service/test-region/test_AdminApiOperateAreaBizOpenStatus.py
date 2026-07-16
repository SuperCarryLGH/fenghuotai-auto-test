import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaBizOpenStatus:
    """更新业务开通状态"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaBizOpenStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/biz-open-status"
        params = {"ids": [common['common']['id']['valid']], "status": common['common']['status']['enabled']}
        resp = api_session.put(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
