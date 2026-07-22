import pytest
from config import ADMIN_URL


class TestInfraDemo01ContactUpdate:
    """更新示例联系人"""

    @pytest.mark.smoke
    def test_InfraDemo01ContactUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo01-contact/update"
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
