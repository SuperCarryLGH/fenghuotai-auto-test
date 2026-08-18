import pytest
import time
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentCreateSettlement(api_session, auth_headers, autotest_supplier, autotest_purchase_order):
    """提交结算申请"""
    supplier_id = autotest_supplier
    order_id = autotest_purchase_order
    body = {
        "supplierId": supplier_id,
        "purchaseOrderIds": [order_id],
        "paymentMethod": 10,
        "invoiceType": 3,
        "invoicePhoto": "",
        "invoiceDate": time.strftime("%Y-%m-%d", time.localtime()),
        "invoiceNo": "",
        "accountName": "张三",
        "bankAccount": "60099928373737382",
        "bankName": "中国建设银行",
        "bankAddress": "杭州西湖支行",
        "remark": "autotest",
    }
    resp = api_session.post(f"{ADMIN_URL}/admin-api/erp/purchase-payment/create-settlement",
                            json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"结算申请提交失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"], "结算申请提交失败，返回 data 为空"
    print(f"结算申请提交成功，付款单id：{data['data']}")
