import pytest
from config import ADMIN_URL


class TestCrmContractSimpleList:
    """获得合同精简列表"""

    @pytest.mark.smoke
    def test_CrmContractSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contract/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
