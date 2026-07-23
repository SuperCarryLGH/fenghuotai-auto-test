import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverHome:
    """司机首页"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverHome(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/home"
        ok(api_session.get(url, headers=auth_headers))
