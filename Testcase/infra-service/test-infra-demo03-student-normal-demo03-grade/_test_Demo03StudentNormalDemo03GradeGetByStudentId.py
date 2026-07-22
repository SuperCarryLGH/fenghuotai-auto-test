import pytest
from config import ADMIN_URL


class TestDemo03StudentNormalDemo03GradeGetByStudentId:
    """获得学生班级"""

    @pytest.mark.smoke
    def test_Demo03StudentNormalDemo03GradeGetByStudentId(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-normal/demo03-grade/get-by-student-id"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
