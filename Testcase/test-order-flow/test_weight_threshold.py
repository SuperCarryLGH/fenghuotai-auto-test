import pytest
from config import TEST_DATA_IDS, TEST_USERS, API_BASE_URL
from Common.DB import USE_MOCK


class TestOrderFlow:
    """验证下单风控链路的重量阈值规则"""

    # ------------------------------------------------------------------
    # TC_073: 单笔重量阈值规则
    # 绑定: 金水区规则 "单笔重量 >10kg 触发送检"
    # ------------------------------------------------------------------
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("weight, expected_status", [
        pytest.param(11.0, "WAIT_CHECK", id="over_10kg_trigger_check"),
        pytest.param(5.0,  "NORMAL",     id="under_10kg_pass"),
    ])
    def test_weight_threshold(
        self, api_session, auth_headers, db_client, weight, expected_status
    ):
        region_id = TEST_DATA_IDS["region"]["henan_zhengzhou_jinshui"]
        fence_id = TEST_DATA_IDS["fence"]["child_fence_b"]
        user_id = TEST_USERS["normal_user"]

        payload = {
            "user_id": user_id,
            "region_id": region_id,
            "fence_id": fence_id,
            "weight": weight,
            "lng": 113.665,
            "lat": 34.789,
        }

        response = api_session.post(
            f"{API_BASE_URL}/order/create", json=payload, headers=auth_headers
        )

        assert response.status_code == 200
        resp = response.json()
        assert resp["code"] == 0

        # Mock 只返回 WAIT_CHECK；非 Mock 时验证真实状态
        if not USE_MOCK:
            assert resp["data"]["status"] == expected_status

            order_no = resp["data"]["order_no"]
            db_result = db_client.fetch_one(
                "SELECT status FROM orders WHERE order_no = %s", (order_no,)
            )
            assert db_result is not None, f"订单 {order_no} 未写入数据库"
            assert db_result["status"] == expected_status