import pytest
from config import APP_URL


class TestSystemDictDataType:
    """根据字典类型查询字典数据信息"""

    @pytest.mark.smoke
    def test_SystemDictDataType(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/system/dict-data/type"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
