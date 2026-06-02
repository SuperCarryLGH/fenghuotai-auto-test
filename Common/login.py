import requests
from config import ADMIN_BASE_URL, APP_BASE_URL, ACCOUNTS, ENV


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

    # TODO: 确认后台登录接口路径和请求体字段
    ADMIN_LOGIN_URL = f"{ADMIN_BASE_URL[ENV]}/auth/login"

    # TODO: 确认后台登录返回的 token 字段路径
    # 当前假设: {"code": 0, "data": {"token": "xxx"}}
    ADMIN_TOKEN_PATH = ("data", "token")

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
        response = self.session.post(self.ADMIN_LOGIN_URL, json=payload)
        response.raise_for_status()
        return self._extract_token(response, self.ADMIN_TOKEN_PATH)

    # ===================================================================
    # APP 用户端登录（普通用户 / 白名单 / 黑名单）
    # ===================================================================

    # TODO: 确认 APP 端登录接口路径
    APP_LOGIN_URL = f"{APP_BASE_URL[ENV]}/auth/login"

    # TODO: 确认 APP 端登录返回值结构
    # 当前假设: {"code": 0, "data": {"token": "xxx"}}
    # 常见情况可能是手机号+验证码登录或账号密码登录
    APP_TOKEN_PATH = ("data", "token")

    def app_login(self, user_id: str = None, mobile: str = None, code: str = None) -> str:
        """
        登录 APP 用户端。

        :param user_id:  用户 ID（用于标识登录者，具体字段视接口而定）
        :param mobile:   手机号（如果是短信验证码登录）
        :param code:     验证码（如果是短信验证码登录）

        TODO: 根据真实 APP 登录接口调整参数和请求体
        """
        # TODO: 替换为真实的 APP 端登录请求体
        payload = {
            "userId": user_id,
            "mobile": mobile,
            "code": code,
        }
        response = self.session.post(self.APP_LOGIN_URL, json=payload)
        response.raise_for_status()
        return self._extract_token(response, self.APP_TOKEN_PATH)
