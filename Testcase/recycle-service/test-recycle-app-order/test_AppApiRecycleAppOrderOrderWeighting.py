import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderOrderWeighting:
    """APP订单称重"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderOrderWeighting(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/app/order/order-weighting"
        body = {"id": order_data['app_order']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
