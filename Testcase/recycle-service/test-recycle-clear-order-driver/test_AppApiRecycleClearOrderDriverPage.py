import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverPage:
    """司机清运单分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverPage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/clear/order/driver/page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
