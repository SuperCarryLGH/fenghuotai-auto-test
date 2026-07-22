import random

import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_yaml


class TestAppSmsLogin:
    """使用手机 + 验证码登录"""

    @pytest.mark.smoke
    def test_batch_app_sms_login(self, api_session):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        users = load_yaml("smk_users.yaml")
        user_list = users.get("smk_users", [])

        print(f"\n共 {len(user_list)} 个用户，开始批量登录...\n")

        results = []
        for user in user_list:
            mobile = user["mobile"]
            desc = user.get("desc", mobile)
            try:
                channel = random.choice(["smk", "szd"])
                payload = {"mobile": mobile, "code": "9999", "channel": channel, "scene": channel,"provider":channel,"platform":"web"}
                resp = api_session.post(
                    f"{APP_URL}/app-api/member/auth/sms-login",
                    json=payload,
                    headers=Login.SMS_LOGIN_HEADERS,
                )
                resp_data = resp.json()
                print(f"  {mobile} 响应: {resp_data}")
                if resp_data.get("code") != 0:
                    raise Exception(resp_data.get("msg", "未知错误"))
                token = resp_data["data"]["accessToken"]
                assert token is not None and len(token) > 0
                results.append({"mobile": mobile, "desc": desc, "token": token, "status": "OK"})
                print(f" 成功 {desc:12s} | {mobile:11s} → {token}")
            except Exception as e:
                results.append({"mobile": mobile, "desc": desc, "token": "", "status": f"FAIL: {e}"})
                print(f" GG {desc:12s} | {mobile:11s} → {e}")

        ok = sum(1 for r in results if r["status"] == "OK")
        fail = len(results) - ok
        print(f"\n批量登录完成: 成功 {ok}，失败 {fail}")
