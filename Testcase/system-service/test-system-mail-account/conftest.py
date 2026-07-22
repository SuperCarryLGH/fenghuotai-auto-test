import time
import pytest
from config import ADMIN_URL


@pytest.fixture(scope="module")
def autotest_mail_account_id(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"mail": "autotest@autotest.com", "username": "autotest_195703", "password": "autotest123", "host": "smtp.autotest.com", "port": 465, "starttlsEnable": False, "sslEnable": False, "status": 0}
    resp = api_session.post(f"{ADMIN_URL}/admin-api/system/mail-account/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    rec_id = data["data"]
    print(f"[Fixture] created autotest_mail_account_id = {rec_id}")

    yield rec_id

    api_session.delete(f"{ADMIN_URL}/admin-api/system/mail-account/delete", params={"id": rec_id}, headers=auth_headers)
    print(f"[Fixture] deleted autotest_mail_account_id = {rec_id}")
