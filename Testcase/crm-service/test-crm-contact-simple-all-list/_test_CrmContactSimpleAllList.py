import pytest
from config import ADMIN_URL


class TestCrmContactSimpleAllList:
    """获得联系人的精简列表"""

    @pytest.mark.smoke
    def test_CrmContactSimpleAllList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contact/simple-all-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
