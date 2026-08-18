import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanPage(api_session, auth_headers, autotest_purchase_plan):
    """获得采购计划分页"""
    plan_id = autotest_purchase_plan
    params = {
        "pageNo": 1,
        "pageSize": 10,
        "id": plan_id,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-plan/page", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划分页查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["total"] >= 1, "采购计划列表信息缺失！"
    ids = [item["id"] for item in data["data"]["list"]]
    assert plan_id in ids, f"分页结果中未包含创建的采购计划：{plan_id}"
    print(f"采购计划列表分页数据：{data['data']}")
