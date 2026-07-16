import pytest
from config import ADMIN_URL


class TestInfraFileConfigTest:
    """测试文件配置是否正确"""

    @pytest.mark.smoke
    def test_InfraFileConfigTest(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/file-config/test"
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
