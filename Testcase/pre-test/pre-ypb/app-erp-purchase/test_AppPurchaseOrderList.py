import pytest
from config import APP_URL


class TestAppPurchaseOrderList:
    """分页查询当前用户的采购订单列表"""

    @pytest.mark.smoke
    def test_list(self, api_session, buyer_headers, ok):
        url = f"{APP_URL}/admin-api/erp/app-purchase-order/list"
        resp = ok(api_session.get(
            url,
            params={"pageNo": 1, "pageSize": 10, "status": "", "supplierName": ""},
            headers=buyer_headers,
        ))
        print(resp)
