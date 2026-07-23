import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleAppTransferOrderCallTransferStatistic:
    """呼叫转运数据统计（在库重量、统货-黑料、前置仓与分拣中心信息）"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderCallTransferStatistic(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/call-transfer-statistic"
        ok(api_session.get(url, headers=auth_headers))
