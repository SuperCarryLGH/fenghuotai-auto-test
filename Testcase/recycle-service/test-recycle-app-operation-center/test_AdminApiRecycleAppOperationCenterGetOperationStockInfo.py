import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiRecycleAppOperationCenterGetOperationStockInfo:
    """查询分拣中心工作台信息"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetOperationStockInfo(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-operation-stock-info"
        params = {
            "operationCenterId":1024
            }

        ok(api_session.get(url, headers=auth_headers,params=params))