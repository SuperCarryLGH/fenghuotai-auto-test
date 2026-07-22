import pytest
from config import ADMIN_URL


class TestDemo03StudentInnerDemo03GradeGetByStudentId:
    """获得学生班级"""

    @pytest.mark.smoke
    def test_Demo03StudentInnerDemo03GradeGetByStudentId(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-inner/demo03-grade/get-by-student-id"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
