import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationListOperationCenter:
    """admin获取回收站点运营中心列表"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationListOperationCenter(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/listOperationCenter"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=auth_headers))
