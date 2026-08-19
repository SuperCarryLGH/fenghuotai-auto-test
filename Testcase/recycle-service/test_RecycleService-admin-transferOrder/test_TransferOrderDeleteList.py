import pytest

from config import ADMIN_URL


class TestTransferOrderDeleteList:
    @pytest.mark.smoke
    def test_TransferOrderDeleteList(self, transfer_order_create, api_session, auth_headers):
        transfer_order_id = transfer_order_create["transfer_order_id"]
        resp = api_session.delete(f"{ADMIN_URL}/admin-api/recycle/transfer-order/delete-list",
                                  params={"ids": [transfer_order_id]}, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0, f"{transfer_order_id}批量删除转运订单失败"
        print(data["data"])
