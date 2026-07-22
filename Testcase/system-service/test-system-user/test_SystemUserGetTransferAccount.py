import pytest
from config import ADMIN_URL


class TestSystemUserGetTransferAccount:
    """查询绑定转账账号"""

    @pytest.mark.smoke
    def test_SystemUserGetTransferAccount(self, api_session, auth_headers, autotest_user_id):
        url = f"{ADMIN_URL}/admin-api/system/user/get-transfer-account"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
