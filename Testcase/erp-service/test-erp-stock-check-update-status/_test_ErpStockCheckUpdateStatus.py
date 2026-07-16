import pytest
from config import ADMIN_URL


class TestErpStockCheckUpdateStatus:
    """更新库存调拨单的状态"""

    @pytest.mark.smoke
    def test_ErpStockCheckUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-check/update-status"
        body = {
            "ids": [],  # TODO: 批量操作的 ID 列表
            "status": 0,  # TODO: 确认状态值
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
