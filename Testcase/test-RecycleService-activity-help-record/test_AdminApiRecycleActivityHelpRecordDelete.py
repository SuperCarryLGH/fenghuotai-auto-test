import pytest
from config import ADMIN_URL
from Common.loader import load_yaml

DATA = load_yaml("help_record.yaml")


class Test_AdminApiRecycleHelpRecordDelete:
    """删除活动助力明细"""

    @pytest.mark.smoke
    def test_AdminApiRecycleHelpRecordDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/delete"
        body = {"id": DATA["id"]}
        resp = api_session.delete(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
