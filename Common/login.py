import requests
from config import API_BASE_URL, ACCOUNTS


class Login:
    """登录工具——获取各类角色 token"""

    # ==========================================
    # TODO: 确认后端登录接口地址和返回字段
    # 提测后替换为真实接口地址
    # ==========================================
    LOGIN_URL = f"{API_BASE_URL}/auth/login"

    # ==========================================
    # TODO: 确认登录接口返回的 token 字段路径
    # 当前假设: {"code": 0, "data": {"token": "xxx"}}
    # ==========================================
    TOKEN_PATH = ("data", "token")

    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _extract_token(self, response: requests.Response) -> str:
        """从登录响应中提取 token，提测后确认字段路径"""
        resp_json = response.json()
        for key in self.TOKEN_PATH:
            resp_json = resp_json[key]
        return resp_json

    def login(self, role: str = "operator") -> str:
        """
        登录指定角色，返回 token

        :param role: 角色名，需在 config.ACCOUNTS 中有对应配置
        """
        if role not in ACCOUNTS:
            raise ValueError(f"未知角色: {role}，可选: {list(ACCOUNTS.keys())}")

        payload = ACCOUNTS[role]
        response = self.session.post(self.LOGIN_URL, json=payload)
        response.raise_for_status()
        return self._extract_token(response)

    def login_admin(self) -> str:
        return self.login("admin")

    def login_operator(self) -> str:
        return self.login("operator")
