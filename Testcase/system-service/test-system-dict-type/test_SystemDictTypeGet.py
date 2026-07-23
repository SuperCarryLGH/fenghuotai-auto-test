import pytest
from config import ADMIN_URL


class TestSystemDictTypeGet:
    """-查询字典类型详细"""

    @pytest.mark.smoke
    def test_SystemDictTypeGet(self, api_session, auth_headers, autotest_dict_type_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/get"
        params = {"id": autotest_dict_type_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
