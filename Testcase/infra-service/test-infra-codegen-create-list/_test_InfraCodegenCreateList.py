import pytest
from config import ADMIN_URL


class TestInfraCodegenCreateList:
    """基于数据库的表结构，创建代码生成器的表和字段定义"""

    @pytest.mark.smoke
    def test_InfraCodegenCreateList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/codegen/create-list"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
