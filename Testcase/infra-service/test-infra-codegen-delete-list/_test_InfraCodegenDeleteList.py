import pytest
from config import ADMIN_URL


class TestInfraCodegenDeleteList:
    """批量删除数据库的表和字段定义"""

    @pytest.mark.smoke
    def test_InfraCodegenDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/codegen/delete-list"
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
