import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class TestNotifyTransfer:
    """转账回调通知"""

    @pytest.mark.smoke
    def test_NotifyTransfer(self, api_session, auth_headers):
        channel_id = common["common"]["id"]["valid"]
        url = f"{ADMIN_URL}/admin-api/pay/notify/transfer/{channel_id}"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
