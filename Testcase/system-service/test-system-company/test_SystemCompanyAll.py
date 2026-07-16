import pytest
from config import ADMIN_URL


class TestSystemCompanyAll:
    """获得全部公司"""

    @pytest.mark.smoke
    def test_SystemCompanyAll(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/company/all"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
