import time
import pytest
from config import APP_URL
from Common.login import Login


@pytest.fixture(scope="module")
def autotest_favorite_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"spuId": 1}
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": auth_headers["Authorization"]}
    resp = api_session.post(f"{APP_URL}/app-api/product/favorite/create", json=body, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_favorite_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{APP_URL}/app-api/product/favorite/delete", params={"id": rec_id}, headers=headers)
    print(f"[Fixture] deleted autotest_favorite_id = {rec_id}")
