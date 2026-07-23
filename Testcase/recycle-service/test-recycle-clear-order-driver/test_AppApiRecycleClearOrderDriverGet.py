import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverGet:
    """司机获取详情"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/get"
        params = {"id": driver_data['driver']['order_id']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
