import time
import pytest
from config import APP_URL
from Common.login import Login


@pytest.fixture(scope="module")
def autotest_record_id(api_session, login_tool):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    token = login_tool.app_login(mobile="15617637160")
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
    body = {}
    resp = api_session.post(f"{APP_URL}/app-api/member/sign-in/record/create", json=body, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_record_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{APP_URL}/app-api/member/sign-in/record/delete", params={"id": rec_id}, headers=headers)
    print(f"[Fixture] deleted autotest_record_id = {rec_id}")
