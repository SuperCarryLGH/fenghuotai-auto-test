import pytest
from config import ADMIN_URL


class TestErpAccountSimpleList:
    """获得结算账户精简列表"""

    @pytest.mark.smoke
    def test_ErpAccountSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/account/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
