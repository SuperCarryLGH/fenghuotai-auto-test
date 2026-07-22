import pytest
from config import ADMIN_URL


class TestDemo03StudentErpDemo03CourseUpdate:
    """更新学生课程"""

    @pytest.mark.smoke
    def test_Demo03StudentErpDemo03CourseUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-erp/demo03-course/update"
        body = {
            "id": 1,  # TODO: 替换为实际 ID，建议用 conftest fixture
            # TODO: 补充更新参数
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
