import pytest
from config import APP_URL


class TestAppPurchaseOrderLoadingDetail:
    """采购订单装车明细"""

    @pytest.mark.smoke
    def test_loading_detail(self, api_session, buyer_headers, ok, autotest_purchase_order):
        url = f"{APP_URL}/admin-api/erp/app-purchase-order/loading-detail"
        resp = ok(api_session.get(url, params={"id": autotest_purchase_order}, headers=buyer_headers))
        print(resp)
