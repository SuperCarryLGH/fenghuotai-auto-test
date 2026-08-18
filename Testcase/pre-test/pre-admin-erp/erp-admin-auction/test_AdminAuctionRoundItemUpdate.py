import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundItemUpdate(api_session, auth_headers, autotest_auction_round_item, autotest_product):
    """修改竞拍商品"""
    item_id = autotest_auction_round_item
    product_id = autotest_product
    body = {
        "id": item_id,
        "roundId": 1,
        "productId": product_id,
        "productCode": "SP001",
        "productName": "商品A",
        "itemName": "商品A-更新",
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
        "remark": "autotest-update",
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/auction-round/item-update", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍商品更新失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, "竞拍商品更新失败"
    print(f"竞拍商品更新成功；{data['data']}")
