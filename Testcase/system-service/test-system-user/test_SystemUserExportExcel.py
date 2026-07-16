import pytest
from config import ADMIN_URL


class TestSystemUserExportExcel:
    """导出用户"""

    @pytest.mark.smoke
    def test_SystemUserExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
