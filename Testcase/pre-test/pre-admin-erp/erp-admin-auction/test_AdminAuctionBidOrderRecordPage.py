import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionBidOrderRecordPage(api_session, auth_headers):
    params = {
        "orderId": 1,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-bid-order/record-page",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍单出价记录查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "竞拍单出价记录返回 data 为空"
    print(f"竞拍单出价记录：{data['data']}")
