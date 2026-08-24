import pytest
from config import APP_URL
#from conftest import purchase_order_complete_shipping

class TestAppPurchaseInWeigh:
    """采购入库称重"""

    @pytest.mark.smoke
    def test_weigh(self, api_session, weigher_headers, ok, autotest_purchase_order):
        #purchase_order_complete_shipping(api_session, autotest_purchase_order)
        url = f"{APP_URL}/admin-api/erp/app-purchase-in/weigh"
        body = {
            "orderId": autotest_purchase_order,
            "warehouseId": 3,
            "vehicleGrossWeight": 2000,
            "vehicleTareWeight": 500,
        }
        resp = ok(api_session.post(url, json=body, headers=weigher_headers))
        print(resp)
