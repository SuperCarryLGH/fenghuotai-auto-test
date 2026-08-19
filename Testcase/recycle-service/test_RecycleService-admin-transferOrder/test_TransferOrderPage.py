import pytest
from pygments.lexers import data

from config import ADMIN_URL
class TestTransferOrderPage:
    @pytest.mark.smoke
    def test_transfer_order_page(self,api_session,auth_headers):
        resp = api_session.get(f"{ADMIN_URL}/admin-api/recycle/transfer-order/page",params={"pageNo":1,"pageSize":10},headers=auth_headers)
        assert resp.status_code == 200
        data=resp.json()
        assert data["code"] == 0,f"转运订单列表信息获取失败"
        print(data["data"])