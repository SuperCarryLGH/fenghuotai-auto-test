import pytest
from config import ADMIN_URL


class TestDemo03StudentNormalDemo03CourseListByStudentId:
    """获得学生课程列表"""

    @pytest.mark.smoke
    def test_Demo03StudentNormalDemo03CourseListByStudentId(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-normal/demo03-course/list-by-student-id"
        params = {
            # TODO: 补充查询参数
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
