import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderCancelClean:
    """APP取消清洁"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderCancelClean(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/cancel-clean"
        body = {"id": order_data['app_order']['order_id']}
        ok(api_session.post(url, json=body, headers=auth_headers))
