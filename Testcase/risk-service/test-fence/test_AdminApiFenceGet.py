import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceGet:
    """admin获取电子围栏详情"""

    @pytest.mark.smoke
    def test_AdminApiFenceGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/fence/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
