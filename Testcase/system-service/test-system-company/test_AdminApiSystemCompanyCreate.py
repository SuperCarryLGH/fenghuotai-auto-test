import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_company

common = load_common()
company_data = load_system_company()


class Test_AdminApiSystemCompanyCreate:
    """创建公司"""

    @pytest.mark.smoke
    def test_AdminApiSystemCompanyCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/company/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{company_data['company']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.post(url, json=body, headers=auth_headers))
