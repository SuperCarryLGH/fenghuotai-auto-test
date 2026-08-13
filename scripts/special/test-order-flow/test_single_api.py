import pytest
from config import ADMIN_URL


@pytest.mark.skip(reason="依赖 member/address/create 前置数据，暂不维护")
class Testsingle_api:
    """获得用户详情"""

    @pytest.mark.smoke
    def test_single_api(self, api_session, auth_headers, autotest_address_id):
        url = f"{ADMIN_URL}/admin-api/system/user/get"
        params = {"id": autotest_address_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
