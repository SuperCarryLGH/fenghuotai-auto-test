import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressUpdate:
    """更新用户收件地址"""

    @pytest.mark.smoke
    def test_MemberAddressUpdate(self, api_session, login_tool, address_id):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/update"
        body = {
            "id": address_id,
            "name": "用户01",
            "mobile": "15617637160",
            "areaId": 330108,
            "detailAddress": "浙江省杭州市滨江区立业园30幢",
            "defaultStatus": True,
        }
        resp = api_session.put(url, json=body, headers=headers)
        assert resp.status_code == 200
