import pytest
from config import ADMIN_URL


class TestBpmProcessDefinitionSimpleList:
    """获得流程定义精简列表"""

    @pytest.mark.smoke
    def test_BpmProcessDefinitionSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-definition/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
