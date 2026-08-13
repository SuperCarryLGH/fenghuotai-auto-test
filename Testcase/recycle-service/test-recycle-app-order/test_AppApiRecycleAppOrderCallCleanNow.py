import pytest
from config import ADMIN_URL


class Test_AppApiRecycleAppOrderCallCleanNow:
    """APP立即呼叫清洁"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                from Common.login import Login
                admin_token = Login(session=api_session).admin_login("admin")
                api_session.delete(
                    f"{ADMIN_URL}/admin-api/recycle/clear-order/delete",
                    params={"id": self._created_id},
                    headers={"tenant-id": "1", "appId": "admin", "sign": "admin",
                             "Authorization": f"Bearer {admin_token}"},
                )
            except Exception as e:
                print(f"[cleanup] 删除清运单 {self._created_id} 失败: {e}")

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderCallCleanNow(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        chain.order_receive(order_id, station_token)
        item_id = chain.order_get_item_id(order_id, station_token)
        chain.order_weigh(order_id, item_id, station_token)
        chain.order_pay(order_id, station_token)
        r = chain.order_call_clean(order_id, station_token)
        self._created_id = (r.get("data") or {}).get("id")
        print(r)
