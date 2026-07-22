import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_level_id(api_session, auth_headers):
    """创建测试等级，返回 ID。先清理残留数据"""
    # 清理上次残留的 autotest 等级
    api_session.delete(f"{ADMIN_URL}/admin-api/member/level/delete",
                       params={"id": "999999999"}, headers=auth_headers)
    
    suffix = str(int(time.time()))[-6:]
    body = {"name": f"autotest_L{suffix}", "level": int(suffix), "experience": int(suffix) * 100, "discountPercent": 100, "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/member/level/create", json=body, headers=auth_headers)
    data = resp.json()
    print(f"[Fixture] level create: code={data.get('code')}, msg={data.get('msg','')}")
    assert resp.status_code == 200
    assert data["code"] == 0
    rec_id = data["data"]
    autotest_level_id.level_num = int(suffix)  # 存 level 编号供 Update 使用
    print(f"[Fixture] created autotest_level_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/member/level/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_level_id = {rec_id}")
