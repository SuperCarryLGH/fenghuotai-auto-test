import pytest
from config import ADMIN_URL


class TestInfraDemo03StudentInnerDeleteList:
    """批量删除学生"""

    @pytest.mark.smoke
    def test_InfraDemo03StudentInnerDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo03-student-inner/delete-list"
        params = {
            "ids": "1,2,3",  # TODO: 替换为实际 ID 列表
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
