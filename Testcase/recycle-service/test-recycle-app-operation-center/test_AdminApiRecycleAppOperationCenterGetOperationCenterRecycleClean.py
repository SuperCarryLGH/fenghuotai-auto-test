import pytest
import time
from config import APP_URL, ADMIN_URL
from Common.loader import load_common
from Common.login import Login

common = load_common()

class Test_AdminApiRecycleAppOperationCenterGetOperationCenterRecycleClean:
    """获取IP对应的地区名"""

    @pytest.mark.skip(reason="APP 账号无 admin-api 权限，待开发排查")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetOperationCenterRecycleClean(self, api_session, login_tool):
        token = login_tool.app_login(mobile="18600000005")
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-operation-center-recycle-clean"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            }

        resp = api_session.get(url, headers=headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
