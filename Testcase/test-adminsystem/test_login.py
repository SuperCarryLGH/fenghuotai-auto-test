import pytest
from Common.login import Login
from config import ADMIN_URL, ACCOUNTS


class TestAdminLogin:
    """后台管理系统 - 登录"""

    @pytest.mark.smoke
    def test_admin_login_success(self, api_session):
        """
        管理员登录
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        # 发原始请求查看完整响应
        url = f"{ADMIN_URL}/admin-api/system/auth/login"
        raw = api_session.post(url, json=ACCOUNTS["admin"], headers={"tenant-id": "1"})
        print(f"\n【状态码】{raw.status_code}")
        print(f"【原始响应】{raw.text}")

        # 再去拿 token 做断言
        login = Login(session=api_session)
        token = login.admin_login("admin")

        assert token is not None
        assert len(token) > 0
        print(f"【提取的 token】{token}")
