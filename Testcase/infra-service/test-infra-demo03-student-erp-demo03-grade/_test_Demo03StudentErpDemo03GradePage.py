import pytest
from config import ADMIN_URL


class TestDemo03StudentErpDemo03GradePage:
    """获得学生班级分页"""

    @pytest.mark.smoke
    def test_Demo03StudentErpDemo03GradePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-erp/demo03-grade/page"
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
