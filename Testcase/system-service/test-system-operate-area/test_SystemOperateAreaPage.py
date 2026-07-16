import pytest
from config import ADMIN_URL


class TestSystemOperateAreaPage:
    """分页查询所有省份（一级）"""

    @pytest.mark.smoke
    def test_SystemOperateAreaPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
