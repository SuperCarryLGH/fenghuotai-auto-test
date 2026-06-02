import sys
import os

# ===============================
# 把项目根目录加入 PYTHONPATH
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ===============================
# 导入 config
# ===============================
from config import API_BASE_URL, ACCOUNTS

import pytest
import requests


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试，核心主流程")
    config.addinivalue_line("markers", "regression: 回归测试，全量覆盖")
    config.addinivalue_line("markers", "slow: 耗时较长的测试")

# ======================
# 1. Session 管理
# ======================
from functools import partial
from unittest.mock import MagicMock


# ======================
# 【Mock 开关】后续删除：删掉 auto_mock 和 mock_* 相关代码即可
# ======================
USE_MOCK = os.getenv("USE_MOCK", "true").lower() in ("1", "true", "yes")


@pytest.fixture(scope="session")
def api_session():
    """
    提供一个全局的 requests.Session 对象
    作用域为整个测试会话，自动携带 Cookie/Header
    """
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.request = partial(session.request, timeout=10)
    yield session
    session.close()


# ======================
# 2. 登录态管理 (Token)
# ======================
from Common.login import Login


@pytest.fixture(scope="session")
def login_tool(api_session):
    """提供 Login 工具实例"""
    return Login(session=api_session)


@pytest.fixture(scope="session")
def admin_token(login_tool):
    """获取超级管理员 Token"""
    return login_tool.login_admin()


@pytest.fixture(scope="function")
def operator_token(login_tool):
    """获取运营人员 Token"""
    return login_tool.login_operator()


@pytest.fixture(scope="function")
def operator_token(api_session):
    """
    获取运营人员 Token
    优先级：P1，用于日常操作
    """
    login_url = f"{API_BASE_URL}/auth/login"
    payload = ACCOUNTS["operator"]
    response = api_session.post(login_url, json=payload)
    response.raise_for_status()
    return response.json()["data"]["token"]


@pytest.fixture(scope="function")
def auth_headers(operator_token):
    """
    提供一个带鉴权的 Header
    这是最常用的 Fixture
    """
    return {"Authorization": f"Bearer {operator_token}"}


# ======================
# 【Mock 区块】后续删除：删掉以下内容到 "# 3. 数据库连接" 为止
# ======================
_MOCK_RESPONSES = {
    f"{API_BASE_URL}/auth/login": {
        "code": 0,
        "data": {"token": "mock_token_auto_test"},
    },
    f"{API_BASE_URL}/order/create": {
        "code": 0,
        "data": {"order_no": "MOCK_ORDER_001", "status": "WAIT_CHECK"},
    },
}


@pytest.fixture(autouse=True, scope="function")
def auto_mock(api_session):
    """USE_MOCK=true 时自动 mock api_session.post 返回固定数据"""
    if not USE_MOCK:
        yield
        return

    original_post = api_session.post

    def mock_post(url, **kwargs):
        if url in _MOCK_RESPONSES:
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = _MOCK_RESPONSES[url]
            return resp
        return original_post(url, **kwargs)

    api_session.post = mock_post
    yield
    api_session.post = original_post


# ======================
# 3. 数据库连接（基于 Common/DB.py 的 DBClient）
# ======================
from Common.DB import DBClient, BizHelper


@pytest.fixture(scope="session")
def db_client():
    """
    提供 DBClient 实例，用于数据库操作与后置校验。
    自动根据 USE_MOCK 决定走真实库还是 Mock。
    """
    try:
        client = DBClient()
        if not USE_MOCK:
            client.conn  # 验证连接
    except Exception:
        client = DBClient()  # 连接失败则用 Mock 保底
    yield client
    client.close()


@pytest.fixture(scope="session")
def biz_helper(db_client):
    """提供 BizHelper 实例，方便业务查询"""
    return BizHelper(db_client)


# ======================
# 4. 测试数据清理 (Hook)
# ======================
@pytest.fixture(autouse=True)
def reset_test_data(db_client):
    """
    【重要】每个测试用例执行前后，重置测试数据
    防止数据污染导致用例失败。
    如果 db_client 处于 Mock 模式，所有操作静默通过。
    """
    # ---- 测试前：清理脏数据 ----
    # TODO 1. 补充你的测试用户 ID
    test_user_ids = ["USER_ID_NORMAL_001", "USER_ID_WHITELIST_001"]

    # TODO 2. 确认下面的表名和字段名
    for uid in test_user_ids:
        db_client.update("user_month_count", {"count": 0}, "user_id = %s", (uid,))

    yield  # 这里执行测试用例

    # ---- 测试后：清理测试产生的垃圾数据 ----
    # TODO 3. 按实际表名补充清理
    # db_client.delete("orders", "is_test = 1")
    # db_client.delete("risk_check_log", "order_no LIKE 'MOCK_%'")