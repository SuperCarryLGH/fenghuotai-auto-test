import pytest
from config import ADMIN_URL


class TestInfraDataSourceConfigList:
    """获得数据源配置列表"""

    @pytest.mark.smoke
    def test_InfraDataSourceConfigList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/data-source-config/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
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
