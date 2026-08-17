import pytest
from config import ADMIN_URL


class TestAppPurchaseOrderList:
    """分页查询当前用户的采购订单列表"""

    @pytest.mark.smoke
    def test_list(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-order/list"
        resp = ok(api_session.get(
            url,
            params={"pageNo": 1, "pageSize": 10, "status": "", "supplierName": ""},
            headers=auth_headers,
        ))
        print(resp)
