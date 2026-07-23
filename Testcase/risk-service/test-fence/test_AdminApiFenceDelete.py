import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceDelete:
    """admin删除电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/fence/delete"
        params = {"id": common['common']['id']['invalid']}
        ok(api_session.delete(url, params=params, headers=auth_headers))
