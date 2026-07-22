import pytest
from config import ADMIN_URL


class TestCrmReceivablePlanSimpleList:
    """获得回款计划精简列表"""

    @pytest.mark.smoke
    def test_CrmReceivablePlanSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/receivable-plan/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
