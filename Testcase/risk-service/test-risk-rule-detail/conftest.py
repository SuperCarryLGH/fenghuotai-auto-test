import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_rule_detail_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"ruleId": int(time.time() * 1000000), "minCount": 1, "maxCount": 2, "actionType": 10, "sort": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/risk/rule-detail/create", json=body, headers=auth_headers)
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:200]}"
    data = resp.json()
    assert data["code"] == 0, f"API error: {data}"
    rec_id = data["data"]
    print(f"[Fixture] created autotest_rule_detail_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/risk/rule-detail/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_rule_detail_id = {rec_id}")
