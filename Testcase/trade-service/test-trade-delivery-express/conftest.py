import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_express_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"code": "AUTOTEST", "name": "autotest_express_195703", "sort": 0, "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/trade/delivery/express/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_express_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/trade/delivery/express/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_express_id = {rec_id}")
