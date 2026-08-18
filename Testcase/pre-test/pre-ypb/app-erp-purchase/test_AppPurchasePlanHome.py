import pytest
from config import APP_URL


class TestAppPurchasePlanHome:
    """采购工作台首页聚合数据"""

    @pytest.mark.smoke
    def test_home(self, api_session, auth_headers, ok):
        url = f"{APP_URL}/admin-api/erp/app-purchase-plan/home"
        resp = ok(api_session.get(url, headers=auth_headers))
        print(resp)
