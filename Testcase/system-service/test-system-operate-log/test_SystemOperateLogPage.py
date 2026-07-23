import pytest
from config import ADMIN_URL


class TestSystemOperateLogPage:
    """查看操作日志分页列表"""

    @pytest.mark.smoke
    def test_SystemOperateLogPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-log/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
