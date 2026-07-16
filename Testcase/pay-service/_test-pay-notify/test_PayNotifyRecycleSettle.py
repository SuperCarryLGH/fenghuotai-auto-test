import pytest
from config import APP_URL


class TestPayNotifyRecycleSettle:
    """回收结算"""

    @pytest.mark.smoke
    def test_PayNotifyRecycleSettle(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/pay/notify/recycle-settle"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
