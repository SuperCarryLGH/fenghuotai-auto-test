import pytest
from config import ADMIN_URL


class TestAppPurchaseOrderCancel:
    """取消采购订单"""

    @pytest.mark.smoke
    def test_cancel(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-order/cancel"
        resp = ok(api_session.post(url, params={"id": autotest_purchase_order}, headers=auth_headers))
        print(resp)
