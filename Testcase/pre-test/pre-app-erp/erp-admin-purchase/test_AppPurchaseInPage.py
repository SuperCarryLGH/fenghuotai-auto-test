import pytest
from config import ADMIN_URL


class TestAppPurchaseInPage:
    """采购入库列表分页"""

    @pytest.mark.smoke
    def test_page(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-in/page"
        resp = ok(api_session.get(
            url,
            params={"pageNo": 1, "pageSize": 10, "keyword": ""},
            headers=auth_headers,
        ))
        print(resp)
