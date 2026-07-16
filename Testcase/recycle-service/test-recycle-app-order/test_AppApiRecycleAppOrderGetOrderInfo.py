import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderGetOrderInfo:
    """APP获取订单信息"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderGetOrderInfo(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/app/order/get-order-info"
        params = {"id": order_data['app_order']['order_id']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
