import pytest
from config import ADMIN_URL


class TestErpAppWarehouseSimpleList:
    """获得分拣中心仓库下拉列表"""

    @pytest.mark.smoke
    def test_ErpAppWarehouseSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/app-warehouse/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
