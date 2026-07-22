import time
import pytest
from config import APP_URL
from Common.login import Login


@pytest.fixture(scope="module")
def autotest_address_id(api_session, login_tool):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    token = login_tool.app_login(mobile="15617637160")
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
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
    resp = api_session.post(f"{APP_URL}/app-api/member/address/create", json=body, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_address_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{APP_URL}/app-api/member/address/delete", params={"id": rec_id}, headers=headers)
    print(f"[Fixture] deleted autotest_address_id = {rec_id}")
