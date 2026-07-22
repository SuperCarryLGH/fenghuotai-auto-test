import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiRecycleAppOperationCenterGetOperationCentorInfo:
    """查询分拣中心工作台信息"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetOperationCentorInfo(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-operation-center-info"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200#test_AdminApiRecycleAppOperationCenterGetOperationCentorInfo
