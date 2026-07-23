import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterWaitingCheckStatistics:
    """admin待验货统计"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterWaitingCheckStatistics(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/waiting-check-statistics"
        ok(api_session.get(url, headers=auth_headers))
