import pytest
from config import ADMIN_URL


class TestCrmBusinessSimpleAllList:
    """获得商机的精简列表"""

    @pytest.mark.smoke
    def test_CrmBusinessSimpleAllList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business/simple-all-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
