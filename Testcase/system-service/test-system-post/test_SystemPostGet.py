import pytest
from config import ADMIN_URL


class TestSystemPostGet:
    """获得岗位信息"""

    @pytest.mark.smoke
    def test_SystemPostGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/post/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
