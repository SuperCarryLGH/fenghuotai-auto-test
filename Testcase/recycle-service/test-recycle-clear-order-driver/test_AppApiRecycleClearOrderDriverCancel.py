import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverCancel:
    """司机取消"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverCancel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/cancel"
        body = {"id": driver_data['driver']['order_id']}
        ok(api_session.post(url, json=body, headers=auth_headers))
