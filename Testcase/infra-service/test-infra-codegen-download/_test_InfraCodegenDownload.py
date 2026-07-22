import pytest
from config import ADMIN_URL


class TestInfraCodegenDownload:
    """下载生成代码"""

    @pytest.mark.smoke
    def test_InfraCodegenDownload(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/codegen/download"
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
