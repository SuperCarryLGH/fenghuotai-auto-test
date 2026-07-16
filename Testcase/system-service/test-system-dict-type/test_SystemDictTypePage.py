import pytest
from config import ADMIN_URL


class TestSystemDictTypePage:
    """获得字典类型的分页列表"""

    @pytest.mark.smoke
    def test_SystemDictTypePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
