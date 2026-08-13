import pytest
from config import ADMIN_URL


class TestPayWalletRechargeCreate:
    """创建钱包充值记录（发起充值）"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, station_token):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/pay/wallet-recharge/delete", params={"id": self._created_id}, headers={"Authorization": f"Bearer {station_token}"})
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_PayWalletRechargeCreate(self, api_session, station_token, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/create"
        body = {
              "payPrice": 50,
              #"packageId": 1024,
              "userType": 2,
              #"bizType": 0,
              #"validPayPriceAndPackageId": True
            }
        resp = api_session.post(url, json=body, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)

