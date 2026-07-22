import pytest
from config import ADMIN_URL


class TestBpmUserGroupSimpleList:
    """获取用户组精简信息列表"""

    @pytest.mark.smoke
    def test_BpmUserGroupSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/user-group/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
