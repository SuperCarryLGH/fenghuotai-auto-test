import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderGetUserTodo(api_session, auth_headers):
    """查询用户待办状态:判断是否完成资质认证、业务签约和缴纳保证金"""
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-auction-bid-order/get-user-todo", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
