import time
import pytest
from config import ADMIN_URL, APP_URL
from config import APP_CONFIG as _APP_CONFIG
from config import ENV as _ENV
from Common.login import Login


def _build_app_headers(app_token):
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {app_token}",
    }


def _resolve_address(api_session, app_headers):
    """Create a test address with area covered by shipping templates"""
    mobile = _APP_CONFIG[_ENV]["accounts"]["normal_user"]["mobile"]
    create_addr_resp = api_session.post(
        f"{APP_URL}/app-api/member/address/create",
        json={
            "name": "测试收件人",
            "mobile": mobile,
            "areaId": 110101,
            "detailAddress": "北京测试地址",
            "defaultStatus": True,
        },
        headers=app_headers,
    )
    if create_addr_resp.status_code != 200:
        pytest.skip("创建地址失败")
    create_addr_data = create_addr_resp.json()
    if create_addr_data["code"] != 0 or not create_addr_data.get("data"):
        pytest.skip(f"创建地址失败: {create_addr_data}")
    return create_addr_data["data"], "测试收件人", mobile


def _create_order(api_session, auth_headers, app_token):
    """Create an unpaid test order, return order_id"""
    app_headers = _build_app_headers(app_token)

    spu_url = f"{ADMIN_URL}/admin-api/product/spu/page"
    all_spus = []
    for page in range(1, 4):
        spu_resp = api_session.get(spu_url, params={"pageNo": page, "pageSize": 20}, headers=auth_headers)
        if spu_resp.status_code != 200:
            break
        spu_data = spu_resp.json()
        if spu_data["code"] != 0 or not spu_data["data"].get("list"):
            break
        all_spus.extend(spu_data["data"]["list"])
    candidates = [
        s for s in all_spus
        if s.get("stock", 0) > 0
        and 1 in (s.get("deliveryTypes") or [])
    ]
    if not candidates:
        pytest.skip("没有可用的商品")

    address_id, receiver_name, receiver_mobile = _resolve_address(api_session, app_headers)

    for spu in candidates:
        detail_resp = api_session.get(
            f"{ADMIN_URL}/admin-api/product/spu/get-detail",
            params={"id": spu["id"]},
            headers=auth_headers,
        )
        if detail_resp.status_code != 200:
            continue
        detail_data = detail_resp.json()
        if detail_data["code"] != 0 or not detail_data["data"].get("skus"):
            continue
        sku = detail_data["data"]["skus"][0]
        delivery_type = (spu.get("deliveryTypes") or [1])[0]

        create_resp = api_session.post(
            f"{APP_URL}/app-api/trade/order/create",
            json={
                "items": [{"skuId": sku["id"], "count": 1}],
                "deliveryType": delivery_type,
                "pointStatus": False,
                "addressId": address_id,
                "receiverName": receiver_name,
                "receiverMobile": receiver_mobile,
            },
            headers=app_headers,
        )
        if create_resp.status_code != 200:
            continue
        create_data = create_resp.json()
        if create_data["code"] != 0:
            continue
        return create_data["data"]["id"]

    pytest.skip("无法创建订单（所有 SPU 无库存或不可用）")


@pytest.fixture
def order_id(api_session, auth_headers, app_token):
    return _create_order(api_session, auth_headers, app_token)
