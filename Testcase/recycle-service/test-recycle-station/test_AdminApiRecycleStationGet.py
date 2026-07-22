import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationGet:
    """admin获取回收站点详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
