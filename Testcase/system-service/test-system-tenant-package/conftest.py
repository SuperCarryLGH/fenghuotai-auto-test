import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_tenant_package_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"name": "autotest_pkg_195703", "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/system/tenant-package/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_tenant_package_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/system/tenant-package/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_tenant_package_id = {rec_id}")
