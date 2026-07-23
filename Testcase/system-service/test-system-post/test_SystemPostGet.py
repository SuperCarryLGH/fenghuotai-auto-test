import pytest
from config import ADMIN_URL


class TestSystemPostGet:
    """获得岗位信息"""

    @pytest.mark.smoke
    def test_SystemPostGet(self, api_session, auth_headers, autotest_post_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/get"
        params = {"id": autotest_post_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
