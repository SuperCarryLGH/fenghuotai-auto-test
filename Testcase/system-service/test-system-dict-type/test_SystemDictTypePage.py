import pytest
from config import ADMIN_URL


class TestSystemDictTypePage:
    """获得字典类型的分页列表"""

    @pytest.mark.smoke
    def test_SystemDictTypePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
