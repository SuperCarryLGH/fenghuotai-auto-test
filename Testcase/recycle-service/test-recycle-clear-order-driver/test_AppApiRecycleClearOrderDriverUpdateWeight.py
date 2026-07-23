import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverUpdateWeight:
    """司机更新重量"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverUpdateWeight(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/update-weight"
        body = {"id": driver_data['driver']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
