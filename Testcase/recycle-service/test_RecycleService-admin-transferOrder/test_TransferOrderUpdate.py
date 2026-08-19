import pytest

from config import ADMIN_URL


class TestTransferOrderUpdate:
    @pytest.mark.smoke
    def test_transferorderupdate(self, transfer_order_create, api_session, auth_headers):
        transfer_order_id = transfer_order_create["transfer_order_id"]
        transfer_order_no = transfer_order_create["orderno"]
        resp = api_session.put(f"{ADMIN_URL}/admin-api/recycle/transfer-order/update",
                               json={"id": transfer_order_id, "transferOrderNo": transfer_order_no},
                               headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0, f"订单：{transfer_order_id}修改信息失败"
        print(data["data"])
