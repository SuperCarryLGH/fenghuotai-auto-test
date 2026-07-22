import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemDictTypePage:
    """获得字典类型的分页列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemDictTypePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
