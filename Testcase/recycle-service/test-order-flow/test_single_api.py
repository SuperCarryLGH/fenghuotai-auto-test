import pytest
from config import ADMIN_URL


class Testsingle_api:
    """获得用户详情"""

    @pytest.mark.smoke
    def test_single_api(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/get"
        params = {"id": autotest_address_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
