import pytest
from config import ADMIN_URL


class TestSystemDictTypeCreate:
    """创建字典类型"""

    @pytest.mark.smoke
    def test_SystemDictTypeCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/create"
        body = {"name": f"测试字典_194199", "type": f"test_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
