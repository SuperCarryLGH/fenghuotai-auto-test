import pytest
import time
from Common.login import Login
from config import APP_URL


class TestMemberSocialUserGetSubscribeTemplateList:
    """获得微信小程订阅模板列表"""

    @pytest.mark.smoke
    def test_MemberSocialUserGetSubscribeTemplateList(self, api_session, login_tool, ok):
        url = f"{APP_URL}/app-api/member/social-user/get-subscribe-template-list"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
