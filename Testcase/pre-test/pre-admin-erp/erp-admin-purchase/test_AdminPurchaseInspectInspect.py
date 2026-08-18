import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchaseInspectInspect(api_session, auth_headers, autotest_purchase_order):
    order_id = autotest_purchase_order
    body = {
        "id": order_id,
        "inspectionStatus": 1,
        "waterDeductionRate": 0.008,
        "waterDeductionWeight": 100,
        "impurityDeductionRate": 0.005,
        "impurityDeductionWeight": 60,
        "inspectionUnitPrice": 200,
        "inspectQualifiedWeight": 12600,
        "inspectQualifiedAmount": 12300,
        "inspectionPicUrls": "",
        "inspectionRemark": "质检通过",
    }
    resp = api_session.post(f"{ADMIN_URL}/admin-api/erp/purchase-inspect/inspect", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购质检提交失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"采购质检提交失败，订单编号：{order_id}"
    print(f"采购质检提交成功；{data['data']}")
