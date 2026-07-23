import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign

common = load_common()
module_data = load_recycle_station_sign()


class Test_AdminApiRecycleStationSignDelete:
    """admin删除回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
