import pytest
from config import ADMIN_URL


class TestErpWarehouseSimpleList:
    """获得仓库精简列表"""

    @pytest.mark.smoke
    def test_ErpWarehouseSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/warehouse/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
