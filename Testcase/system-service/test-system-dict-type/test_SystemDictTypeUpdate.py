import pytest
from config import ADMIN_URL


class TestSystemDictTypeUpdate:
    """修改字典类型"""

    @pytest.mark.smoke
    def test_SystemDictTypeUpdate(self, api_session, auth_headers, autotest_dict_type_id):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/update"
        body = {"id": autotest_dict_type_id, "name": "autotest_updated", "type": "autotest", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
