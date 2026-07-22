import pytest
from config import ADMIN_URL


class TestCrmBusinessStatusStatusSimpleList:
    """获得商机状态列表"""

    @pytest.mark.smoke
    def test_CrmBusinessStatusStatusSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business-status/status-simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
