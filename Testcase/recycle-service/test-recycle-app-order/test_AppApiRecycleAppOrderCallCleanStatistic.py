import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderCallCleanStatistic:
    """APP呼叫清洁统计"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderCallCleanStatistic(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/call-clean-statistic"
        ok(api_session.get(url, headers=auth_headers))
