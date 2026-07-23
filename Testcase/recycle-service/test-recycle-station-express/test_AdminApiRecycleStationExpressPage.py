import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressPage:
    """admin回收站快递单分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
