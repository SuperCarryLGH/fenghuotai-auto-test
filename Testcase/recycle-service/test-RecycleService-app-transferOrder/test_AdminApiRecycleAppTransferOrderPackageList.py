import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderPackageList:
    """转运单包裹分页列表"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderPackageList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/package-list"
        params ={
            "transferOrderId": transfer["transfer"]['transferOrderId'],
            "pageNo": transfer["transfer"]['pageNo'],
            "pageSize": transfer["transfer"]['pageSize'],
            }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
