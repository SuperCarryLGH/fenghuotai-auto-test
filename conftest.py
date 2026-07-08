import sys
import os
import warnings

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
USE_MOCK = os.getenv("USE_MOCK", "true").lower() in ("1", "true", "yes")


@pytest.fixture(scope="session")
def api_session():
    """
    提供一个全局的 requests.Se ssion 对象
    作用域为整个测试会话，自动携带 Cookie/Header
    """
    session = requests.Session()
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
# 【Mock 区块】后续删除：删掉以下内容到 "# 3. 数据库连接" 为止
# ======================
_MOCK_URLS = {
    f"{APP_URL}/app-api/member/auth/send-sms-code",
    f"{APP_URL}/app-api/cooperation/getByPlatform",
    f"{APP_URL}/app-api/recycle/activity/list",
    f"{APP_URL}/app-api/recycle/activity/my/list",
    f"{APP_URL}/app-api/recycle/station/detail",
    f"{APP_URL}/order/create",
    #f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
    f"{APP_URL}/app-api/recycle/order/station-order-submit",
    f"{ADMIN_URL}/admin-api/member/tag/create",
    f"{ADMIN_URL}/admin-api/member/level-record/get",
    f"{ADMIN_URL}/admin-api/member/level-record/page",
    f"{ADMIN_URL}/admin-api/member/experience-record/get",
    f"{ADMIN_URL}/admin-api/member/experience-record/page",
    f"{ADMIN_URL}/admin-api/member/config/get",
    f"{ADMIN_URL}/admin-api/member/config/save",
    f"{ADMIN_URL}/admin-api/member/user/get",
    f"{ADMIN_URL}/admin-api/member/user/page",
    f"{ADMIN_URL}/admin-api/member/user/update",
    f"{ADMIN_URL}/admin-api/member/user/update-level",
    f"{ADMIN_URL}/admin-api/member/user/update-point",
    f"{ADMIN_URL}/admin-api/member/sign-in/config/create",
    f"{ADMIN_URL}/admin-api/member/sign-in/config/delete",
    f"{ADMIN_URL}/admin-api/member/sign-in/config/get",
    f"{ADMIN_URL}/admin-api/member/sign-in/config/list",
    f"{ADMIN_URL}/admin-api/member/sign-in/config/update",
    f"{ADMIN_URL}/admin-api/member/point/record/page",
    f"{ADMIN_URL}/admin-api/member/sign-in/record/page",
    f"{ADMIN_URL}/admin-api/member/social-user/wxa-qrcode",
    f"{ADMIN_URL}/admin-api/member/group/create",
    f"{ADMIN_URL}/admin-api/member/group/delete",
    f"{ADMIN_URL}/admin-api/member/group/get",
    f"{ADMIN_URL}/admin-api/member/group/listallsimple",
    f"{ADMIN_URL}/admin-api/member/group/page",
    f"{ADMIN_URL}/admin-api/member/group/update",
    f"{ADMIN_URL}/admin-api/member/addresss/list",
    f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/call-transfer-now",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/add-package",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/call-transfer-statistic",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/cancel",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/get",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/loading-complete",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/package-list",
    f"{APP_URL}/admin-api/recycle/app-transferOrder/page",
    f"{APP_URL}/admin-api/recycle/app-clearOrder-weigher/get-transfer-stockin-detail",
    f"{ADMIN_URL}/admin-api/pay/recharge/get",
    f"{ADMIN_URL}/admin-api/pay/recharge/page",
    f"{ADMIN_URL}/admin-api/pay/withdraw/page",
    f"{ADMIN_URL}/admin-api/pay/withdraw/get",
    f"{ADMIN_URL}/admin-api/pay/withdraw/audit",
}

_MOCK_RESPONSES = {
    f"{ADMIN_URL}/admin-api/system/auth/login": {
        "code": 0, "data": {"accessToken": "mock_admin_token"},
    },
    f"{APP_URL}/app-api/member/auth/sms-login": {
        "code": 0, "data": {"accessToken": "mock_app_token"},
    },
    f"{APP_URL}/app-api/recycle/activity/group/detail": {
        "code": 0, "msg": "success", "data": {"id": 0},
    },
    #f"{APP_URL}/app-api/member/address/create": {
     #   "code": 0, "msg": "", "data": "MOCK_ADDR_ID",
    #},
    f"{ADMIN_URL}/admin-api/member/tag/create": {
        #"code": 0, "msg": "", "data": 0,
    },
    f"{ADMIN_URL}/admin-api/member/level-record/get": {
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/level-record/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/experience-record/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/experience-record/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/config/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/config/save":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/user/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/user/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/user/update":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/user/update-level":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/user/update-point":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/config/create":{
        "code": 0, "msg": "", "data": 0,
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/config/delete":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/config/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/config/list":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/config/update":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/point/record/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/sign-in/record/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/social-user/wxa-qrcode":{
        "code": 0, "msg": "", "data": "",
    },
    f"{ADMIN_URL}/admin-api/member/group/create":{
        "code": 0, "msg": "", "data": 0
    },
    f"{ADMIN_URL}/admin-api/member/group/delete":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/group/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/group/listallsimple":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/group/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/member/group/update":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{ADMIN_URL}/admin-api/member/addresss/list":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/call-transfer-now":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/add-package":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/call-transfer-statistic":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/cancel":{
        "code": 0, "msg": "", "data": "true",
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/loading-complete":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/package-list":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-transferOrder/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{APP_URL}/admin-api/recycle/app-clearOrder-weigher/get-transfer-stockin-detail":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/pay/recharge/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/pay/recharge/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/pay/withdraw/page":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/pay/withdraw/get":{
        "code": 0, "msg": "", "data": {},
    },
    f"{ADMIN_URL}/admin-api/pay/withdraw/audit":{
        "code": 0, "msg": "", "data": {},
    },
}


@pytest.fixture(autouse=True, scope="session")
def auto_mock(api_session):
    """USE_MOCK=true 时拦截所有 HTTP 请求，返回固定数据"""
    if not USE_MOCK:
        yield
        return

    original_request = api_session.request

    def mock_request(method, url, **kwargs):
        if url in _MOCK_RESPONSES:
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = _MOCK_RESPONSES[url]
            return resp
        if url in _MOCK_URLS:
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = {"code": 0, "msg": "success", "data": {}}
            return resp
        return original_request(method, url, **kwargs)

    api_session.request = mock_request
    yield
    api_session.request = original_request


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
    _users = load_users().get("users", {})
    test_user_ids = [u["id"] for u in _users.values() if "id" in u]
    # TODO: 确认 user_id 值是否正确

    # TODO 2. 确认下面的表名和字段名
    for uid in test_user_ids:
        db_client.update("user_month_count", {"count": 0}, "user_id = %s", (uid,))

    yield  # 这里执行测试用例

    # ---- 测试后：清理测试产生的垃圾数据 ----
    # TODO 3. 按实际表名补充清理
    # db_client.delete("orders", "is_test = 1")
    # db_client.delete("risk_check_log", "order_no LIKE 'MOCK_%'")