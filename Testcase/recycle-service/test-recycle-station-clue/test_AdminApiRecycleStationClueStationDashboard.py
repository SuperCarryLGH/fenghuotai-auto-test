import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueStationDashboard:
    """admin站点仪表盘"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueStationDashboard(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-dashboard"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
