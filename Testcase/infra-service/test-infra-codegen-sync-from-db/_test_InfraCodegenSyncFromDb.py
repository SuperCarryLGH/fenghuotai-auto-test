import pytest
from config import ADMIN_URL


class TestInfraCodegenSyncFromDb:
    """基于数据库的表结构，同步数据库的表和字段定义"""

    @pytest.mark.smoke
    def test_InfraCodegenSyncFromDb(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/codegen/sync-from-db"
        body = {
            # TODO: 补充请求体参数
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
