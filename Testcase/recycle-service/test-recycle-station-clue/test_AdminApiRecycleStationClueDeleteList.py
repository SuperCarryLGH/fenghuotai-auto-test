import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleStationClueDeleteList:
    """admin批量删除网点线索"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueDeleteList(self, api_session, station_user_ctx):
        b_headers, _, _ = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/delete-list"
        params = {"ids": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=b_headers)

        assert resp.status_code == 200
