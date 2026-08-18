import pytest
import time
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanUpdate(api_session, auth_headers, autotest_purchase_plan, autotest_product):
    """更新采购计划"""
    plan_id = autotest_purchase_plan
    product_id = autotest_product
    body = {
        "id": plan_id,
        "title": "测试采购计划-更新",
        "planDate": time.strftime("%Y-%m-%d", time.localtime()),
        "planEndDate": time.strftime("%Y-%m-%d", time.localtime()),
        "targetQuantity": 200,
        "estimatedPrice": 20,
        "status": 10,
        "items": [{"productId": product_id, "targetQuantity": 200}],
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-plan/update", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划更新失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"采购计划更新失败，编号：{plan_id}"
    print(f"采购计划更新成功；{data['data']}")
