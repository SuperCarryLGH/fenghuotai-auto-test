import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressCreate:
    """创建用户收件地址"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, login_tool):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                token = login_tool.app_login(mobile="15204643417")
                headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
                api_session.delete(f"{APP_URL}/app-api/member/address/delete", params={"id": self._created_id}, headers=headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_MemberAddressCreate(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15204643417")
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
            "mobile": "18900000002",
            "areaId": 330381,
            "defaultStatus": True,
        }
        r = ok(api_session.post(url, json=body, headers=headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
        print(r)
