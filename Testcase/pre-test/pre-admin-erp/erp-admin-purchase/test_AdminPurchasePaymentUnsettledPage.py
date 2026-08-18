import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentUnsettledPage(api_session, auth_headers):
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-payment/unsettled-page",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"未结算列表查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["total"] >= 0, "未结算列表信息缺失！"
    print(f"未结算列表分页数据：{data['data']}")
