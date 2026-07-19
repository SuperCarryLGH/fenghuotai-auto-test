import pytest
from config import ADMIN_URL


class TestPayChannelGetEnableCodeList:
    """获得指定应用的开启的支付渠道编码列表"""

    @pytest.mark.smoke
    def test_PayChannelGetEnableCodeList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/channel/get-enable-code-list"
        params = {
            "appId" : 2077228704176402434
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
