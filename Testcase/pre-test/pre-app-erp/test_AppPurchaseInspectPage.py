import pytest
from config import ADMIN_URL


class TestAppPurchaseInspectPage:
    """采购质检列表分页"""

    @pytest.mark.smoke
    def test_page(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/erp/purchase-inspect/page"
        resp = ok(api_session.get(
            url,
            params={"inspectType": 0, "pageNo": 1, "pageSize": 10},
            headers=auth_headers,
        ))
        print(resp)
