import pytest
from config import ADMIN_URL


class TestInfraDemo02CategoryCreate:
    """创建示例分类"""

    @pytest.mark.smoke
    def test_InfraDemo02CategoryCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo02-category/create"
        body = {
            # TODO: 补充创建参数
            # 示例: "name": f"autotest_182356", "status": 0,
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
