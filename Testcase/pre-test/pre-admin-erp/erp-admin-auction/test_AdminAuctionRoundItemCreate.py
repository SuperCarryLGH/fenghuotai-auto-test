import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundItemCreate(api_session, auth_headers, autotest_auction_round, autotest_product):
    round_id = autotest_auction_round
    product_id = autotest_product
    body = {
        "id": 0,
        "roundId": round_id,
        "productId": product_id,
        "productCode": "SP001",
        "productName": "商品A",
        "itemName": "商品A",
        "productCategoryId": 1,
        "productCategoryName": "分类A",
        "productUnitId": 1,
        "productUnitName": "KG",
        "availableStock": 1000,
        "packageCount": 10,
        "operationCenterId": 1,
        "operationCenterName": "分拣中心A",
        "productCoverImage": "",
        "productCarouselImages": [],
        "totalQuantity": 500,
        "startPrice": 10,
        "qualityLevel": "A",
        "initialBidCount": 0,
        "itemDescription": "",
        "sort": 0,
        "remark": "autotest",
    }
    resp = api_session.post(f"{ADMIN_URL}/admin-api/erp/auction-round/item-create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍商品创建失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"], "竞拍商品创建失败，返回 data 为空"
    print(f"竞拍商品创建成功，id：{data['data']}")
