import pytest
from config import APP_URL


class TestAppPurchaseOrderDetail:
    """采购订单详情"""

    @pytest.mark.smoke
    def test_detail(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{APP_URL}/admin-api/erp/app-purchase-order/detail"
        resp = ok(api_session.get(url, params={"id": autotest_purchase_order}, headers=auth_headers))
        print(resp)
