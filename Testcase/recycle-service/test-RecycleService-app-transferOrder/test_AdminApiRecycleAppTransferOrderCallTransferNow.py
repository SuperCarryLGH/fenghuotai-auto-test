import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderCallTransferNow:
    """立即呼叫转运"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderCallTransferNow(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/call-transfer-now"
        params ={
            "warehouseId": transfer["transfer"]['warehouseId'],
            "operationCenterId": transfer["transfer"]['operationCenterId'],
            "appointmentTimePeriod": transfer["transfer"]['appointmentTimePeriod'],
            "appointmentDate": transfer["transfer"]['appointmentDate'],
            "appointmentWeekStr": transfer["transfer"]['appointmentWeekStr'],
            "transferType": transfer["transfer"]['transferType'],
        }
        ok(api_session.post(url, json=params, headers=auth_headers))
