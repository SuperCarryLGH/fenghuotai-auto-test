import pytest
from config import ADMIN_URL


class TestDemo03StudentErpDemo03CourseGet:
    """获得学生课程"""

    @pytest.mark.smoke
    def test_Demo03StudentErpDemo03CourseGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-erp/demo03-course/get"
        params = {
            "id": 1,  # TODO: 替换为实际存在的 ID
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
