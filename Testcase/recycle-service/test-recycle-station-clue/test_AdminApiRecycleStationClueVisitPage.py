import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleStationClueVisitPage:
    """admin回访分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueVisitPage(self, api_session, station_user_ctx, ok):
        b_headers, _, _ = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=b_headers))
