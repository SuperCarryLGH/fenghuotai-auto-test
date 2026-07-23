import pytest
from config import ADMIN_URL


class TestSystemDictTypeDelete:
    """删除字典类型"""

    @pytest.mark.smoke
    def test_SystemDictTypeDelete(self, api_session, auth_headers, autotest_dict_type_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/delete"
        params = {"id": autotest_dict_type_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
