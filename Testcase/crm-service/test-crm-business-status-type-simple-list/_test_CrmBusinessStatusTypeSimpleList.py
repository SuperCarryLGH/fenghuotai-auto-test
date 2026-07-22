import pytest
from config import ADMIN_URL


class TestCrmBusinessStatusTypeSimpleList:
    """获得商机状态组列表"""

    @pytest.mark.smoke
    def test_CrmBusinessStatusTypeSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business-status/type-simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
