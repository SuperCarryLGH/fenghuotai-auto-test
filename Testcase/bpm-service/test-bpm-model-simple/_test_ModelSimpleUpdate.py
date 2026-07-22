import pytest
from config import ADMIN_URL


class TestModelSimpleUpdate:
    """保存仿钉钉流程设计模型"""

    @pytest.mark.smoke
    def test_ModelSimpleUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/model/simple/update"
        body = {
            # TODO: 补充创建参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
