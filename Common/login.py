import requests
from config import ADMIN_URL, APP_URL, ACCOUNTS


class Login:
    """
    登录工具——支持管理后台和 APP 两端登录。

    用法:
        login = Login(session)
        admin_token = login.admin_login("admin")
        operator_token = login.admin_login("operator")
        user_token = login.app_login("normal_user")
    """

    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ===================================================================
    # 管理后台登录（配置规则 / 日常运营）
    # ===================================================================
    ADMIN_LOGIN_URL = f"{ADMIN_URL}/admin-api/system/auth/login"

    # Headers 附加参数（多租户系统需要传租户 ID）
    ADMIN_LOGIN_HEADERS = {"tenant-id": "1"}

    # 返回结构: {"code": 0, "data": {"accessToken": "xxx", ...}}
    ADMIN_TOKEN_PATH = ("data", "accessToken")

    def _extract_token(self, response: requests.Response, path: tuple) -> str:
        """从登录响应中按路径提取 token"""
        resp_json = response.json()
        print(f"\n[DEBUG] 登录响应: {resp_json}", flush=True)
        data = resp_json
        for key in path:
            data = data[key]
        return data

    def admin_login(self, role: str = "operator") -> str:
        """
        登录后台管理端。

        :param role: 角色名，需在 config.ACCOUNTS 中有对应配置
        """
        if role not in ACCOUNTS:
            raise ValueError(f"未知角色: {role}，可选: {list(ACCOUNTS.keys())}")

        payload = ACCOUNTS[role]
        return self.admin_login_with(**payload)

    def admin_login_with(self, username: str, password: str) -> str:
        """
        使用自定义账号密码登录后台管理端。

        :param username: 用户名
        :param password: 密码
        """
        payload = {"username": username, "password": password}
        response = self.session.post(
            self.ADMIN_LOGIN_URL,
            json=payload,
            headers=self.ADMIN_LOGIN_HEADERS,
        )
        response.raise_for_status()
        return self._extract_token(response, self.ADMIN_TOKEN_PATH)

    # ===================================================================
    # APP 用户端登录（短信验证码登录）
    # 请求头中的 appId/sign/nonce/timestamp 模拟 APP 端签名
    # ===================================================================
    SMS_LOGIN_URL = f"{APP_URL}/app-api/member/auth/sms-login"

    SMS_LOGIN_HEADERS = {
        "tenant-id": "1",
        "appId": "admin",
        "sign": "admin",
        "terminal": "31",
        "platform": "App",
        "nonce": "866413",
        "timestamp": "1780650379429",
    }

    APP_TOKEN_PATH = ("data", "accessToken")

    def app_login(self, mobile: str = None, code: str = "9999") -> str:
        """
        APP 短信验证码登录。

        :param mobile: 手机号，默认从 users.yaml 读取 normal_user.mobile
        :param code: 验证码，默认 9999
        """
        if mobile is None:
            from Common.loader import load_users
            mobile = load_users()["users"]["normal_user"]["mobile"]
        return self.app_login_with(mobile, code)

    def app_login_with(self, mobile: str, code: str = "9999") -> str:
        """
        使用自定义手机号登录 APP 端。

        :param mobile: 手机号
        :param code: 验证码，默认 9999
        """
        payload = {"mobile": mobile, "code": code}
        response = self.session.post(
            self.SMS_LOGIN_URL, json=payload, headers=self.SMS_LOGIN_HEADERS,
        )
        response.raise_for_status()
        return self._extract_token(response, self.APP_TOKEN_PATH)
