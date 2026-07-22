import pytest
from config import ADMIN_URL


class TestErpPurchaseReturnGet:
    """获得采购退货"""

    @pytest.mark.smoke
    def test_ErpPurchaseReturnGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/purchase-return/get"
        params = {
            "id": 1,  # TODO: 替换为实际存在的 ID
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
