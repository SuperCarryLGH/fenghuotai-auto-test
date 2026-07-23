import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverParcelProductOptions:
    """司机包裹产品选项"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverParcelProductOptions(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/parcel-product-options"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
