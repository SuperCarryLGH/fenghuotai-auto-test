import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundUpdate(api_session, auth_headers, autotest_auction_round, autotest_product):
    """更新竞拍场次"""
    round_id = autotest_auction_round
    product_id = autotest_product
    body = {
        "id": round_id,
        "auctionName": "测试竞拍场次-更新",
        "auctionType": 1,
        "startTime": "",
        "endTime": "",
        "coverImage": "",
        "description": "autotest-update",
        "status": 1,
        "remark": "autotest-update",
        "items": [
            {
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
                "remark": "autotest-update",
            }
        ],
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/auction-round/update", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍场次更新失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, "竞拍场次更新失败"
    print(f"竞拍场次更新成功；{data['data']}")
