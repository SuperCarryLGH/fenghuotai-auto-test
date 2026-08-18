import pytest
from config import APP_URL


class TestAppPurchaseInStockRecordPage:
    """采购入库库存记录分页"""

    @pytest.mark.smoke
    def test_stock_record_page(self, api_session, auth_headers, ok):
        url = f"{APP_URL}/admin-api/erp/app-purchase-in/stock-record/page"
        resp = ok(api_session.get(
            url,
            params={"pageNo": 1, "pageSize": 10, "keyword": ""},
            headers=auth_headers,
        ))
        print(resp)
