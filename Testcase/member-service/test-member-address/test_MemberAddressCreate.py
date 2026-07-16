import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressCreate:
    """创建用户收件地址"""

    @pytest.mark.smoke
    def test_MemberAddressCreate(self, api_session, login_tool):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/create"
        body = {
            "name": "用户01",
            "mobile": "15617637160",
            "areaId": 330108,
            "detailAddress": "浙江省杭州市滨江区立业园",
            "defaultStatus": True,
        }
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
