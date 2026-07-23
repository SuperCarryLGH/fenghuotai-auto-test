import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign

common = load_common()
module_data = load_recycle_station_sign()


class Test_AdminApiRecycleStationSignDeleteList:
    """admin批量删除回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/delete-list"
        params = {"ids": [common['common']['id']['invalid']]}
        ok(api_session.delete(url, params=params, headers=auth_headers))
