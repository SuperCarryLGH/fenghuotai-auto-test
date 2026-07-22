import pytest
from config import ADMIN_URL


class TestSystemDictDataCreate:
    """新增字典数据"""

    @pytest.mark.smoke
    def test_SystemDictDataCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/create"
        body = {"label": f"测试数据_194199", "value": f"test_194199", "dictType": "test", "sort": 0, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
