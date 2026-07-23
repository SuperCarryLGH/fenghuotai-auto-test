import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderCancel:
    """前置仓取消转运"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderCancel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-transferOrder/cancel"
        params ={
            "id": transfer["transfer"]['id']
            }
        resp = api_session.post(url, json=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
