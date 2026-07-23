import pytest
from config import ADMIN_URL


class TestSystemDictTypeDeleteList:
    """批量删除字典类型"""

    @pytest.mark.smoke
    def test_SystemDictTypeDeleteList(self, api_session, auth_headers, autotest_dict_type_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/delete-list"
        params = {"ids": str(autotest_dict_type_id)}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
