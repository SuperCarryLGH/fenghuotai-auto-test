import pytest
from config import ADMIN_URL


class TestSystemDictDataDeleteList:
    """批量删除字典数据"""

    @pytest.mark.smoke
    def test_SystemDictDataDeleteList(self, api_session, auth_headers, autotest_dict_data_id):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/delete-list"
        params = {"ids": str(autotest_dict_data_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
