import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderCallCleanStatistic:
    """APP呼叫清洁统计"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderCallCleanStatistic(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/app/order/call-clean-statistic"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
