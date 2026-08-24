import pytest
from config import APP_URL


class TestAppPurchaseInspectPage:
    """采购质检列表分页"""

    @pytest.mark.smoke
    def test_page(self, api_session, inspector_headers, ok):
        url = f"{APP_URL}/admin-api/erp/purchase-inspect/page"
        resp = ok(api_session.get(
            url,
            params={"inspectType": 0, "pageNo": 1, "pageSize": 10},
            headers=inspector_headers,
        ))
        print(resp)
