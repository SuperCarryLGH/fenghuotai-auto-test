import pytest
from config import APP_URL


class TestPayNotifyStationWithdraw:
    """站点提现通知"""

    @pytest.mark.smoke
    def test_PayNotifyStationWithdraw(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/pay/notify/station-withdraw"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
