import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationDelete:
    """admin删除回收站点"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
