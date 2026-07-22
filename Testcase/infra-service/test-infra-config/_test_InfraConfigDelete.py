import pytest
from config import ADMIN_URL


class TestInfraConfigDelete:
    """删除参数配置"""

    @pytest.mark.smoke
    def test_InfraConfigDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/config/delete"
        params = {
            "id": 1,  # TODO: 替换为实际要删除的 ID，或改为 conftest fixture
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
