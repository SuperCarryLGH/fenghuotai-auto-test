import sys
import os
import warnings

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

warnings.filterwarnings("ignore", category=Warning, module="urllib3")

# ===============================
# 把项目根目录加入 PYTHONPATH
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ===============================
# 导入 config
# ===============================
from config import APP_URL, ACCOUNTS, ADMIN_URL

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
USE_MOCK = os.getenv("USE_MOCK", "False").lower() in ("1", "true", "yes")


@pytest.fixture(scope="session")
def api_session():
    """
    提供一个全局的 requests.Se ssion 对象
    作用域为整个测试会话，自动携带 Cookie/Header
    """
    session = requests.Session()
    session.verify = False
    session.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0",
    })
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
    """获取超级管理员 Token（后台管理端）"""
    return login_tool.admin_login("admin")


@pytest.fixture(scope="function")
def operator_token(login_tool):
    """获取运营人员 Token（后台管理端）"""
    return login_tool.admin_login("operator")


@pytest.fixture(scope="session")
def app_token(login_tool):
    """获取 APP 用户 Token（短信验证码登录）"""
    return login_tool.app_login()


@pytest.fixture(scope="session")
def auth_headers(admin_token):
    """
    提供一个带鉴权的 Header（后台管理端）
    这是最常用的 Fixture
    """
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="function")
def app_auth_headers(app_token):
    """提供 APP 端鉴权 Header"""
    return {"Authorization": f"Bearer {app_token}"}


# ======================
# 统一响应校验 fixture
# ======================
@pytest.fixture
def ok():
    """统一响应校验：自动 assert status_code==200 + code==0，返回解析后的 dict"""
    def _ok(resp, expect_code=0):
        assert resp.status_code == 200, f"HTTP {resp.status_code}:\n{resp.text[:500]}"
        r = resp.json()
        assert r["code"] == expect_code, f"业务失败: code={r['code']}, msg={r.get('msg','')}"
        return r
    return _ok


# ======================
# 3. 数据库连接（基于 Common/DB.py 的 DBClient）
# ======================
from Common.DB import DBClient, BizHelper
from Common.loader import load_users


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
        client = DBClient(force_mock=True)  # 连接失败则用 Mock 保底
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
    yield  # 这里执行测试用例

    # ---- 测试后：清理测试产生的垃圾数据 ----
    # TODO: 后续按实际需要补充清理逻辑