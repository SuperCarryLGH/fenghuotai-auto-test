import pytest
from config import ADMIN_URL


class TestInfraDemo03StudentErpPage:
    """获得学生分页"""

    @pytest.mark.smoke
    def test_InfraDemo03StudentErpPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-erp/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
