import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderGet:
    """转运订单详情"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/get"
        params ={
            "id": transfer["transfer"]['id']
            }
        ok(api_session.get(url, params=params, headers=auth_headers))
