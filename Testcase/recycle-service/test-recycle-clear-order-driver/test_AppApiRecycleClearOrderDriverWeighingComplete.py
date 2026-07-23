import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverWeighingComplete:
    """司机称重完成"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverWeighingComplete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/weighing-complete"
        body = {"id": driver_data['driver']['order_id']}
        ok(api_session.post(url, json=body, headers=auth_headers))
