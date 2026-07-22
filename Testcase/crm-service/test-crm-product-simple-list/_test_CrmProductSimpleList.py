import pytest
from config import ADMIN_URL


class TestCrmProductSimpleList:
    """获得产品精简列表"""

    @pytest.mark.smoke
    def test_CrmProductSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/product/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
