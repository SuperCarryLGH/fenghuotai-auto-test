import pytest
from config import APP_URL


class TestAppPurchaseInDetail:
    """采购入库详情"""

    @pytest.mark.smoke
    def test_detail(self, api_session, weigher_headers, ok, autotest_purchase_in):
        url = f"{APP_URL}/admin-api/erp/app-purchase-in/detail"
        resp = ok(api_session.get(url, params={"id": autotest_purchase_in}, headers=weigher_headers))
        print(resp)
