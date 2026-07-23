import pytest
from config import ADMIN_URL


class TestSystemPostUpdate:
    """修改岗位"""

    @pytest.mark.smoke
    def test_SystemPostUpdate(self, api_session, auth_headers, autotest_post_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/update"
        body = {"id": autotest_post_id, "name": "autotest_updated", "code": "autotest_code", "sort": 0, "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
