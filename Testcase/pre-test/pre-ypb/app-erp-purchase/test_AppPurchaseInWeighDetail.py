import pytest
from config import APP_URL


class TestAppPurchaseInWeighDetail:
    """采购入库称重详情"""

    @pytest.mark.smoke
    def test_weigh_detail(self, api_session, weigher_headers, ok, autotest_purchase_order):
        print(autotest_purchase_order)
        url = f"{APP_URL}/admin-api/erp/app-purchase-in/weigh/detail"
        resp = ok(api_session.get(url, params={"orderId": autotest_purchase_order}, headers=weigher_headers))
        print(resp)
