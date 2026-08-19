import pytest

from config import ADMIN_URL


class TestTransferOrderGet:
    @pytest.mark.smoke
    def test_transferorderget(self, transfer_order_create, api_session, auth_headers):
        transfer_order_id = transfer_order_create["transfer_order_id"]
        resp = api_session.get(f"{ADMIN_URL}/admin-api/recycle/transfer-order/get",
                               params={"id": transfer_order_id}, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0, f"{transfer_order_id}转运单信息获取失败"
        print(data["data"])
