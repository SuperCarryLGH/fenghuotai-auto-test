import pytest
from config import ADMIN_URL


class TestSystemCompanyGet:
    """获得公司信息"""

    @pytest.mark.smoke
    def test_SystemCompanyGet(self, api_session, auth_headers, autotest_company_id):
        url = f"{ADMIN_URL}/admin-api/system/company/get"
        params = {"id": autotest_company_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
