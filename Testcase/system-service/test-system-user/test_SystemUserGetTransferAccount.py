import pytest
from config import ADMIN_URL


class TestSystemUserGetTransferAccount:
    """查询绑定转账账号"""

    @pytest.mark.smoke
    def test_SystemUserGetTransferAccount(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/get-transfer-account"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
