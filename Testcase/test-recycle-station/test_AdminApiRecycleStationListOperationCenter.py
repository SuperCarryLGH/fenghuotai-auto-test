import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationListOperationCenter:
    """admin获取回收站点运营中心列表"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationListOperationCenter(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/list-operation-center"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.post(url, json=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
