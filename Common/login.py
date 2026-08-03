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
        self.session.verify = False
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
        if resp_json.get("code") != 0:
            raise RuntimeError(
                f"Login failed: code={resp_json.get('code')}, "
                f"msg={resp_json.get('msg')}, data={resp_json.get('data')}"
            )
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
            verify=False,
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
        "timestamp": "",   # 每次登录时动态更新
    }

    APP_TOKEN_PATH = ("data", "accessToken")

    # ===================================================================
    # 短信验证码发送
    # ===================================================================
    SMS_SEND_URL = f"{APP_URL}/app-api/member/auth/send-sms-code"

    def send_sms_code(self, mobile: str, scene: int = 1) -> bool:
        """
        发送短信验证码。

        :param mobile: 手机号
        :param scene: 场景值，默认 1（登录）
        :return: 是否发送成功
        """
        import time
        self.SMS_LOGIN_HEADERS["timestamp"] = str(int(time.time() * 1000))
        resp = self.session.post(
            self.SMS_SEND_URL,
            json={"mobile": mobile, "scene": scene},
            headers=self.SMS_LOGIN_HEADERS,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()["code"] == 0

    def app_login(self, mobile: str = None, code: str = "9999") -> str:
        """
        APP 短信验证码登录。

        :param mobile: 手机号，默认从 users.yaml 读取 normal_user.mobile
        :param code: 验证码，默认 9999（dev 环境免验证码）
        全局开关: config.USE_REAL_SMS_CODE=True 则先发短信再输入真实验证码
        """
        from config import USE_REAL_SMS_CODE
        if mobile is None:
            from Common.loader import load_users
            mobile = load_users()["users"]["normal_user"]["mobile"]
        return self.app_login_with(mobile, code, USE_REAL_SMS_CODE)

    def app_login_with(self, mobile: str, code: str = "9999", use_real_code: bool = None) -> str:
        """
        使用自定义手机号登录 APP 端。

        :param mobile: 手机号
        :param code: 验证码，默认 9999
        :param use_real_code: None=读 config.USE_REAL_SMS_CODE; True/False=手动覆盖
        """
        import time
        if use_real_code is None:
            from config import USE_REAL_SMS_CODE
            use_real_code = USE_REAL_SMS_CODE
        if use_real_code:
            # 先发送验证码
            self.send_sms_code(mobile)
            print(f"\n[Login] 已发送验证码至 {mobile}，请在手机上查收")
            if code == "9999":
                import os
                code = os.getenv("SMS_CODE") or input(f"[Login] 请输入 {mobile} 收到的验证码: ").strip()
        self.SMS_LOGIN_HEADERS["timestamp"] = str(int(time.time() * 1000))
        payload = {"mobile": mobile, "code": code}
        response = self.session.post(
            self.SMS_LOGIN_URL, json=payload, headers=self.SMS_LOGIN_HEADERS,
            verify=False,
        )
        response.raise_for_status()
        return self._extract_token(response, self.APP_TOKEN_PATH)

    def app_login_for_promoter(self, mobile: str, code: str = "9999", promoter_id: int = None) -> str:
        """
        APP 登录，支持推广员邀请码绑定（不影响现有 app_login 逻辑）。

        :param mobile: 手机号
        :param code: 验证码，默认 9999
        :param promoter_id: 邀请人推广ID（首次登录时绑定上下级关系）
        """
        import time
        self.SMS_LOGIN_HEADERS["timestamp"] = str(int(time.time() * 1000))
        payload = {"mobile": mobile, "code": code}
        if promoter_id:
            payload["promoterId"] = promoter_id
        response = self.session.post(
            self.SMS_LOGIN_URL,
            json=payload,
            headers=self.SMS_LOGIN_HEADERS,
            verify=False,
        )
        response.raise_for_status()
        return self._extract_token(response, self.APP_TOKEN_PATH)
