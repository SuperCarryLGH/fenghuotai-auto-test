import pytest


class Test_TransferOrderCreate:
    @pytest.mark.smoke
    def test_TransferOrderCreate(self, transfer_order_create):
        transfer_order_id = transfer_order_create["transfer_order_id"]
        assert transfer_order_id, "转运单创建失败"
        print(f"转运单创建成功: {transfer_order_id}")
