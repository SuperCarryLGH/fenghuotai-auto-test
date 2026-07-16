import pytest
from config import ADMIN_URL


class TestSystemMailTemplateUpdate:
    """修改邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/update"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
