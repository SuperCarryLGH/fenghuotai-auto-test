import pytest
from config import ADMIN_URL


class TestSystemDictTypeSimpleList:
    """获得全部字典类型列表"""

    @pytest.mark.smoke
    def test_SystemDictTypeSimpleList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/simple-list"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
