import pytest
from config import ADMIN_URL


class TestSystemLoginLogExportExcel:
    """导出登录日志 Excel"""

    @pytest.mark.smoke
    def test_SystemLoginLogExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/login-log/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
