import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AppApiRecycleAppOrderPageStation:
    """APP站点分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPageStation(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/page-station"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=auth_headers))
