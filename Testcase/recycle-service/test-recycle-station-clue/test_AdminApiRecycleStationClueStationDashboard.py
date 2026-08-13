import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueStationDashboard:
    """admin站点仪表盘"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="线索/签约业务流字段契约未完全确认(网点ID/拜访意向/运行状态等)，待补")
    def test_AdminApiRecycleStationClueStationDashboard(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-dashboard"
        ok(api_session.get(url, params={"stationId": 1}, headers=auth_headers))
