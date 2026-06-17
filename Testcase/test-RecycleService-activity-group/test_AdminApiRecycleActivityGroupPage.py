import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_page,load_users

common = load_common()
page = load_page()
users = load_users()


class Test_AdminApiRecycleActivityGroupPage:
    """获得活动组分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityGroupPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-group/page"
        body = {
            "pageNo": page["page"]["pageNo"],
            "pageSize": page["page"]["pageSize"],
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
