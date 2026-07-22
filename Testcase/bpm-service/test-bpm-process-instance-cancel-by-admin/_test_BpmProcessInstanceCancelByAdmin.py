import pytest
from config import ADMIN_URL


class TestBpmProcessInstanceCancelByAdmin:
    """管理员取消流程实例"""

    @pytest.mark.smoke
    def test_BpmProcessInstanceCancelByAdmin(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/cancel-by-admin"
        params = {
            "id": 1,  # TODO: 替换为实际 ID
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
