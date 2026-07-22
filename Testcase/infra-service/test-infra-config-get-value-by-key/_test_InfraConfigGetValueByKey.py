import pytest
from config import ADMIN_URL


class TestInfraConfigGetValueByKey:
    """根据参数键名查询参数值"""

    @pytest.mark.smoke
    def test_InfraConfigGetValueByKey(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/config/get-value-by-key"
        params = {
            # TODO: 补充查询参数
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
