import pytest
from config import ADMIN_URL


class TestAppPurchaseInWeighDetail:
    """采购入库称重详情"""

    @pytest.mark.smoke
    def test_weigh_detail(self, api_session, auth_headers, ok, autotest_purchase_order):
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-in/weigh/detail"
        resp = ok(api_session.get(url, params={"orderId": autotest_purchase_order}, headers=auth_headers))
        print(resp)
