import pytest
from config import ADMIN_URL


class TestInfraDemo01ContactGet:
    """获得示例联系人"""

    @pytest.mark.smoke
    def test_InfraDemo01ContactGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/demo01-contact/get"
        params = {
            "id": 1,  # TODO: 替换为实际存在的 ID
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
