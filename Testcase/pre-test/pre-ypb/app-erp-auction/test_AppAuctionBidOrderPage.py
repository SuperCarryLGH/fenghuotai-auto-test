import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderPage(api_session, auth_headers):
    """获得APP端竞拍场次分页列表:仅返回【待开始】和【竞拍中】状态的竞拍场次，按【竞拍中】优先、同状态按结束时间升序排序"""
    params = {"pageNo": 1, "pageSize": 10}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-auction-bid-order/page", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
