import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressGet:
    """admin获取回收站快递单详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
