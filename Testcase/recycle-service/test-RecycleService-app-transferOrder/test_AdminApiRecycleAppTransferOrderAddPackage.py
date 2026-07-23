import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderAddPackage:
    """扫码新增转运包裹"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderAddPackage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/add-package"
        params ={
            "transferOrderId": transfer["transfer"]['transferOrderId'],
            "packageNo": transfer["transfer"]['packageNo'],
        }
        resp = api_session.post(url, json=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
