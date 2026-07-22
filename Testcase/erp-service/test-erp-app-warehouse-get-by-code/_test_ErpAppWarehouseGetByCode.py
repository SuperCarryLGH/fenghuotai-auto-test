import pytest
from config import ADMIN_URL


class TestErpAppWarehouseGetByCode:
    """根据仓库码获得仓库"""

    @pytest.mark.smoke
    def test_ErpAppWarehouseGetByCode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/app-warehouse/get-by-code"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
