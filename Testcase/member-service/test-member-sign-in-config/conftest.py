import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_config_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    day = int(time.time()) % 365
    # 幂等：先删该 day 的旧配置，避免跨运行残留导致 1004009001(已存在)
    lst = api_session.get(f"{ADMIN_URL}/admin-api/member/sign-in/config/list",
                          headers=auth_headers).json().get("data") or []
    for item in lst:
        if str(item.get("day")) == str(day):
            api_session.delete(f"{ADMIN_URL}/admin-api/member/sign-in/config/delete",
                               params={"id": item["id"]}, headers=auth_headers)
    body = {"day": day, "point": 10, "experience": 10, "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/member/sign-in/config/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"创建签到配置失败: code={data.get('code')} msg={data.get('msg')}"
    rec_id = data["data"]
    print(f"[Fixture] created autotest_config_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/member/sign-in/config/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_config_id = {rec_id}")
