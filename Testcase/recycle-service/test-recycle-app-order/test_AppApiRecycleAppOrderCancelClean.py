import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderCancelClean:
    """APP取消清洁"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="接口请求方法未确认(405)，且需真实订单数据")
    def test_AppApiRecycleAppOrderCancelClean(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/cancel-clean"
        body = {"id": order_data['app_order']['order_id']}
        ok(api_session.post(url, json=body, headers=auth_headers))
