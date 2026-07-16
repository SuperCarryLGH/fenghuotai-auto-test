import pytest
from config import APP_URL


class TestMemberSocialUserGetSubscribeTemplateList:
    """获得微信小程订阅模板列表"""

    @pytest.mark.smoke
    def test_MemberSocialUserGetSubscribeTemplateList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/social-user/get-subscribe-template-list"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
