import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanCreate(api_session, auth_headers, autotest_product):
    product_id = autotest_product
    body = {
        "id": 0,
        "title": "测试采购计划",
        "planDate": "",
        "planEndDate": "",
        "targetQuantity": 100,
        "estimatedPrice": 10,
        "status": 10,
        "items": [{"productId": product_id, "targetQuantity": 100}],
    }
    resp = api_session.post(f"{ADMIN_URL}/admin-api/erp/purchase-plan/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划创建失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"], "采购计划创建失败，返回 data 为空"
    print(f"采购计划创建成功，id：{data['data']}")
