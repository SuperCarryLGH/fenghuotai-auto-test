import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueStationStatus:
    """线索站点状态"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="线索/签约业务流字段契约未完全确认(网点ID/拜访意向/运行状态等)，待补")
    def test_AdminApiRecycleStationClueStationStatus(self, clue_chain, api_session, ok):
        chain, clue_id, clue_no, auth_headers = clue_chain
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-status"
        r = ok(api_session.put(url, json={"stationId": 1, "status": 0}, headers=auth_headers))
        print(r)
