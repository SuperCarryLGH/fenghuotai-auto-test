import time
import pytest
from config import APP_URL


@pytest.fixture(scope="module")
def autotest_order_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"name": "autotest_195703", "status": 0}
    resp = api_session.post(f"{APP_URL}/app-api/trade/order/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_order_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{APP_URL}/app-api/trade/order/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_order_id = {rec_id}")
