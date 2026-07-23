import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderLoadingComplete:
    """装车完成"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderLoadingComplete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/loading-complete"
        params ={
            "id": transfer["transfer"]['id'],
            "driverName": transfer["transfer"]['driverName'],
            "driverPhone": transfer["transfer"]['driverPhone'],
            "driverLicensePlateNumber": transfer["transfer"]['driverLicensePlateNumber'],
            "loadPicUrls": transfer["transfer"]['loadPicUrls']
            }
        ok(api_session.post(url, json=params, headers=auth_headers))
