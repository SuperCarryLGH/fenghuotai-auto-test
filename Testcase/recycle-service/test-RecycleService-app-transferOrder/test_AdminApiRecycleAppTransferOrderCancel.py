import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderCancel:
    """前置仓取消转运"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderCancel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/cancel"
        params ={
            "id": transfer["transfer"]['id']
            }
        ok(api_session.post(url, json=params, headers=auth_headers))
