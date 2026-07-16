import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_page

common = load_common()
page = load_page()


class Test_AppApiRecycleOrderPage:
    """查询小程序订单分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleOrderPage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/order/page"
        params = {
            "pageNo": page['page']['pageNo'],
            "pageSize": page['page']['pageSize'],
            "status":page['status']['status6']
                  }
        resp = api_session.get(url, params=params, headers=auth_headers)
        print(resp.text)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
