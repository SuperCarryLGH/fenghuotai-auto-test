import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_page,load_users

common = load_common()
page = load_page()
users = load_users()


class Test_AdminApiRecycleActivityGroupGet:
    """获取互动组"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityGroupGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-group/get"
        body = {
            "id": 9999,
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
