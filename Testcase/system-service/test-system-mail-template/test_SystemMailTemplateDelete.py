import pytest
from config import ADMIN_URL


class TestSystemMailTemplateDelete:
    """删除邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
