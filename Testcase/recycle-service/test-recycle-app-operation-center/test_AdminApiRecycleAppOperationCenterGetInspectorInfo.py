import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiRecycleAppOperationCenterGetInspectorInfo:
    """获取IP对应的地区名"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetInspectorInfo(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-inspector-info"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200#test_AdminApiSystemAreaGetByIp








