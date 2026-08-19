import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleStationCluePage:
    """admin网点线索分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationCluePage(self, api_session, station_user_ctx, ok):
        b_headers, _, _ = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=b_headers))
