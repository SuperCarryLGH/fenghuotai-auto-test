import time
import pytest
from config import ADMIN_URL
from Common.login import Login


@pytest.fixture(scope="module")
def station_token(api_session):
    """通过 ADMIN SMS 登录获取 18600000000 的后台 token（有站点权限）"""
    headers = {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
    }
    resp = api_session.post(
        f"{ADMIN_URL}/admin-api/system/auth/sms-login",
        json={"mobile": "18600000000", "code": "9999"},
        headers=headers,
    )
    assert resp.status_code == 200
    token = resp.json()["data"]["accessToken"]
    print(f"[Fixture] station_token = {token[:10]}...")
    return token
