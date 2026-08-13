import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterManagerInspectUser:
    """admin管理员验货人员"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="接口请求方法未确认(405)，且需真实包裹数据")
    def test_AdminApiRecycleAppOperationCenterManagerInspectUser(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/manager-inspect-user"
        body = {"id": 1}
        ok(api_session.post(url, json=body, headers=auth_headers))
