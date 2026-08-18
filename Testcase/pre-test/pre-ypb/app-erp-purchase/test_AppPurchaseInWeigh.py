import pytest
from config import APP_URL


class TestAppPurchaseInWeigh:
    """采购入库称重"""

    @pytest.mark.smoke
    def test_weigh(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{APP_URL}/admin-api/erp/app-purchase-in/weigh"
        body = {
            "orderId": autotest_purchase_order,
            "warehouseId": 3,
            "vehicleGrossWeight": 2000,
            "vehicleTareWeight": 500,
        }
        resp = ok(api_session.post(url, json=body, headers=auth_headers))
        print(resp)
