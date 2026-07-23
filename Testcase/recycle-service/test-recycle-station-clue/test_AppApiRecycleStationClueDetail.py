import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AppApiRecycleStationClueDetail:
    """APP线索详情"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationClueDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/get"
        params = {"id": clue_data['station_clue']['id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
