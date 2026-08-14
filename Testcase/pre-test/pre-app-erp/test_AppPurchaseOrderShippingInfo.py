import pytest
from config import ADMIN_URL


class TestAppPurchaseOrderShippingInfo:
    """采购订单运输信息"""

    @pytest.mark.smoke
    def test_shipping_info(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-order/shipping-info"
        resp = ok(api_session.get(url, params={"id": autotest_purchase_order}, headers=auth_headers))
        print(resp)
