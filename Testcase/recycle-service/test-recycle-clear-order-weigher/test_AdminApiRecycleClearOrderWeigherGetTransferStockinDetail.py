import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleClearOrderWeigherGetTransferStockinDetail:
    """转运入库详情（转运单信息、包裹汇总、运输信息、始发-终点）"""

    @pytest.mark.skip(reason="待补充合法业务数据")
    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherGetTransferStockinDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/get-transfer-stockin-detail"
        params = {
            "id": 1
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
