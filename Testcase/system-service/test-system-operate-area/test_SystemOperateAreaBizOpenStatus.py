import pytest
from config import ADMIN_URL


class TestSystemOperateAreaBizOpenStatus:
    """更新业务开通状态"""

    @pytest.mark.smoke
    def test_SystemOperateAreaBizOpenStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/biz-open-status"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
