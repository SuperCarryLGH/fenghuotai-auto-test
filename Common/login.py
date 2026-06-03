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
        data = response.json()
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
        response = self.session.post(
            self.ADMIN_LOGIN_URL,
            json=payload,
            headers=self.ADMIN_LOGIN_HEADERS,
        )
        response.raise_for_status()
        return self._extract_token(response, self.ADMIN_TOKEN_PATH)

    # ===================================================================
    # APP 用户端登录（微信小程序手机号登录）
    # ===================================================================
    APP_LOGIN_URL = f"{APP_URL}/app-api/member/auth/weixin-mini-app-login"

    APP_LOGIN_HEADERS = {"tenant-id": "1"}

    APP_TOKEN_PATH = ("data", "accessToken")

    def app_login(self, phone_code: str, login_code: str,
                  state: str = "test-state-001",
                  uuid: str = "test-device-001",
                  device_data: str = "iPhone") -> str:
        payload = {
            "phoneCode": phone_code,
            "loginCode": login_code,
            "state": state,
            "uuid": uuid,
            "deviceData": device_data,
        }
        response = self.session.post(
            self.APP_LOGIN_URL, json=payload, headers=self.APP_LOGIN_HEADERS,
        )
        response.raise_for_status()
        return self._extract_token(response, self.APP_TOKEN_PATH)
