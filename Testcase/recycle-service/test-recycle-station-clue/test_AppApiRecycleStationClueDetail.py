import pytest
from config import ADMIN_URL


class Test_AppApiRecycleStationClueDetail:
    """APP 线索详情"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationClueDetail(self, clue_chain, api_session, ok):
        chain, clue_id, clue_no, auth_headers = clue_chain
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/get"
        r = ok(api_session.get(url, params={"id": clue_id}, headers=auth_headers))
        print(r)
