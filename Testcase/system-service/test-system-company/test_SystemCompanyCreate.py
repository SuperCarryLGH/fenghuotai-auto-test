import pytest
from config import ADMIN_URL


class TestSystemCompanyCreate:
    """创建公司"""

    @pytest.mark.smoke
    def test_SystemCompanyCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/company/create"
        body = {"name": f"测试公司_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
