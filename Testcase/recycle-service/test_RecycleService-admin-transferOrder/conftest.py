import pytest
import time
from config import ADMIN_URL
from Common.DB import query_one

Transfer = f"{ADMIN_URL}/admin-api/recycle"


@pytest.fixture
def transfer_order_create(api_session, auth_headers):
    orderno = f"TO{int(time.time() * 1000)}"
    body = {
        "id": 0,
        "userId": 2074701659722608641,
        "transferOrderNo": orderno,
    }
    resp = api_session.post(f"{Transfer}/transfer-order/create", json=body, headers=auth_headers)
    assert resp.status_code == 200, f"HTTP {resp.status_code}:\n{resp.text[:500]}"
    r = resp.json()
    assert r["code"] == 0, f"业务失败: code={r.get('code')}, msg={r.get('msg', '')}"

    row = query_one(
        "SELECT id FROM recycle_transfer_order WHERE transfer_order_no=%s", (orderno,))
    assert row, f"DB 未查到转运单 {orderno}"
    transfer_order_id = row["id"]
    yield {"transfer_order_id": transfer_order_id, "orderno": orderno}
    try:
        api_session.delete(f"{Transfer}/transfer-order/delete",
                           params={"id": transfer_order_id}, headers=auth_headers)
    except Exception as e:
        print(f"[cleanup] 删除转运单 {transfer_order_id} 失败: {e}")
