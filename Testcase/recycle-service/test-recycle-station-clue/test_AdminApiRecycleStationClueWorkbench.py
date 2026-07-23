import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueWorkbench:
    """admin工作台"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueWorkbench(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/workbench"
        ok(api_session.get(url, headers=auth_headers))
