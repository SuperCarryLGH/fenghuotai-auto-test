import pytest
from config import ADMIN_URL
class TestTransferOrderExcel:
    @pytest.mark.smoke
    def test_TransferOrderExcel(self,api_session,auth_headers):
        resp = api_session.get(f"{ADMIN_URL}/admin-api/recycle/transfer-order/export-excel",params={"pageNo":1,"pageSize":10},headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.content) > 0