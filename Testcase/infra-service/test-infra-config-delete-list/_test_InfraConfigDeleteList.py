import pytest
from config import ADMIN_URL


class TestInfraConfigDeleteList:
    """批量删除参数配置"""

    @pytest.mark.smoke
    def test_InfraConfigDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/config/delete-list"
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
