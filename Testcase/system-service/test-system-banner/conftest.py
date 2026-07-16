import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_banner_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"title": "autotest_banner_195703", "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/system/banner/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_banner_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/system/banner/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_banner_id = {rec_id}")
