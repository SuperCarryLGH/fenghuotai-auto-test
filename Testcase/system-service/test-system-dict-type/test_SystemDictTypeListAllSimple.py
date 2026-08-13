import pytest
from config import ADMIN_URL


class TestSystemDictTypeListAllSimple:
    """获得全部字典类型列表"""

    @pytest.mark.smoke
    def test_SystemDictTypeListAllSimple(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/list-all-simple"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
