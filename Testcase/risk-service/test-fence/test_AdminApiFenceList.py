import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceList:
    """admin获取电子围栏列表"""

    @pytest.mark.smoke
    def test_AdminApiFenceList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/fence/list"
        ok(api_session.get(url, headers=auth_headers))
