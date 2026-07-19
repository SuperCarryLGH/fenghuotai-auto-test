import pytest
from config import APP_URL


class TestPayNotifyUserWithdraw:
    """用户提现通知"""

    @pytest.mark.smoke
    def test_PayNotifyUserWithdraw(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/pay/notify/user-withdraw"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
