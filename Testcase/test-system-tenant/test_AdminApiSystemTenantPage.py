import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_tenant

common = load_common()
tenant_data = load_system_tenant()


class Test_AdminApiSystemTenantPage:
    """admin租户分页"""

    @pytest.mark.smoke
    def test_AdminApiSystemTenantPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/tenant/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            "code": tenant_data['tenant']['create']['code'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
