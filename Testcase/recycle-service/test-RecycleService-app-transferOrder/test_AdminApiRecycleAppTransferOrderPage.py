import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderAddPage:
    """前置仓转运单分页列表"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderAddPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/page"
        params ={
            "status": transfer["transfer"]['status'],
            "pageNo": transfer["transfer"]['packageNo'],
            "pageSize": transfer["transfer"]['pageSize']
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
