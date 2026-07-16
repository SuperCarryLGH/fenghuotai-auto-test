import pytest
from config import ADMIN_URL


class TestSystemDictDataListAllSimple:
    """获得全部字典数据列表"""

    @pytest.mark.smoke
    def test_SystemDictDataListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
