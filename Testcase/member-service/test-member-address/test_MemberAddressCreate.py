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
            "province": "浙江省",
            "provinceCode": "330000",
            "cityCode": "330300",
            "areaName": "浙江省 温州市 瑞安市",
            "city": "温州市",
            "district": "瑞安市",
            "districtCode": "330381",
            "communityName": "恒逸温州仓",
            "detailAddress": "世纪大道与导航路交叉口西北方向57米左右恒逸",
            "name": "恒逸温州仓",
            "mobile": "15617637160",
            "areaId": 330381,
            "defaultStatus": True,
        }
        resp = api_session.post(url, json=body, headers=headers)
        r = resp.json()
        print(r)
        assert resp.status_code == 200
        assert r["code"] == 0, f"创建地址失败: {r}"
