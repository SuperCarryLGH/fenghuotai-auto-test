import pytest
from config import ADMIN_URL


class TestInfraApiErrorLogPage:
    """获得 API 错误日志分页"""

    @pytest.mark.smoke
    def test_InfraApiErrorLogPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/api-error-log/page"
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
