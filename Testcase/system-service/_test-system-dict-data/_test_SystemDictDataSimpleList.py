import pytest
from config import ADMIN_URL


class TestSystemDictDataSimpleList:
    """获得全部字典数据列表"""

    @pytest.mark.smoke
    def test_SystemDictDataSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
