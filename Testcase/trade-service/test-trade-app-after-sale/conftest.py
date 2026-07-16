import time
import pytest
from config import APP_URL


@pytest.fixture(scope="module")
def autotest_after_sale_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"orderItemId": 1, "way": 1, "refundPrice": 100, "applyReason": "autotest"}
    resp = api_session.post(f"{APP_URL}/app-api/trade/after-sale/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_after_sale_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{APP_URL}/app-api/trade/after-sale/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_after_sale_id = {rec_id}")
