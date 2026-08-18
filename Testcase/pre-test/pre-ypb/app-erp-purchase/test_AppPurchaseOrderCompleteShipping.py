import pytest
from config import APP_URL


class TestAppPurchaseOrderCompleteShipping:
    """完成发货（推进订单状态：待发货 → 待到厂）"""

    @pytest.mark.smoke
    def test_complete_shipping(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{APP_URL}/admin-api/erp/app-purchase-order/complete-shipping"
        resp = ok(api_session.post(url, params={"id": autotest_purchase_order}, headers=auth_headers))
        print(resp)
