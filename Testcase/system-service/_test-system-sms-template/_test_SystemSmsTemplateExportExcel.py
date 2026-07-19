import pytest
from config import ADMIN_URL


class TestSystemSmsTemplateExportExcel:
    """导出短信模板 Excel"""

    @pytest.mark.smoke
    def test_SystemSmsTemplateExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-template/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
