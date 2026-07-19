import pytest
from config import ADMIN_URL


class TestPayNotifyGetDetail:
    """获得回调通知的明细"""

    @pytest.mark.smoke
    def test_PayNotifyGetDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/notify/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
