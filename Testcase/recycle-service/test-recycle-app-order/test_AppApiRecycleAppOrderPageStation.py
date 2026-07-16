import pytest
from config import APP_URL
from Common.loader import load_common

common = load_common()


class Test_AppApiRecycleAppOrderPageStation:
    """APP站点分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPageStation(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/app/order/page-station"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
