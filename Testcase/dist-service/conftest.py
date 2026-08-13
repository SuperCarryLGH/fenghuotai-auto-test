"""推广达人测试 fixtures"""
import time
import pytest
from Common.login import Login


@pytest.fixture(scope="session")
def promoter_headers(login_tool):
    """推广申请/排行/钱包"""
    token = login_tool.app_login(mobile="15606103874")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture(scope="session")
def promoterinfo_headers(login_tool):
    """推广信息/实名/签约"""
    token = login_tool.app_login(mobile="15610173675")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture(scope="session")
def rulepersonal_headers(login_tool):
    """分销规则"""
    token = login_tool.app_login(mobile="15610173675")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }
