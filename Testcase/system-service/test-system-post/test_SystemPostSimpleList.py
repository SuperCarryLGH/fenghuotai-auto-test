import pytest
from config import ADMIN_URL


class TestSystemPostSimpleList:
    """获取岗位全列表"""

    @pytest.mark.smoke
    def test_SystemPostSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/post/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
