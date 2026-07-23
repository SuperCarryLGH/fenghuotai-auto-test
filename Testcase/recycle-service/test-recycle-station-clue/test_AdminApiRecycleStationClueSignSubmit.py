import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueSignSubmit:
    """admin签约提交"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueSignSubmit(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/sign-submit"
        body = {"id": common['common']['id']['valid']}
        ok(api_session.post(url, json=body, headers=auth_headers))
