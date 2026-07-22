import json
import os
import pytest
from config import APP_URL
from Common.login import Login

ORDER_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-order-flow", "last_order.json")


class TestRecycleOrderCancel:
    """回收订单取消 — 依赖 mini-order-submit 创建的订单"""

    @pytest.mark.smoke
    def test_RecycleOrderCancel(self, api_session, login_tool):
        # 读取 mini-order-submit 保存的 orderId
        if not os.path.exists(ORDER_FILE):
            pytest.skip(f"未找到订单文件 {ORDER_FILE}，请先运行 test_mini_order_submit")

        with open(ORDER_FILE) as f:
            order_data = json.load(f)
        order_id = order_data["orderId"]
        print(f"读取订单: order_id={order_id}")

        token = login_tool.app_login(mobile="15617600003")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/order/cancel"
        body = {
            "orderId": order_id,
            "cancelReason": "用户主动取消",
            "cancelType": 0,
        }
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(f"取消成功: {r}")
