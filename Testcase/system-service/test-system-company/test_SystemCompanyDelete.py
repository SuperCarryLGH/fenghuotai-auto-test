import pytest
from config import ADMIN_URL


class TestSystemCompanyDelete:
    """删除公司"""

    @pytest.mark.smoke
    def test_SystemCompanyDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/company/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
