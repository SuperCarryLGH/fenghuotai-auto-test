import pytest
from config import ADMIN_URL


class TestSystemPostUpdate:
    """修改岗位"""

    @pytest.mark.smoke
    def test_SystemPostUpdate(self, api_session, auth_headers, autotest_post_id):
        url = f"{ADMIN_URL}/admin-api/system/post/update"
        body = {"id": autotest_post_id, "name": "autotest_updated", "code": "autotest_code", "sort": 0, "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
