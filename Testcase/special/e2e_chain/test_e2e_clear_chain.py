"""
清运结算全链路 E2E 测试
站点呼叫清运 → 司机接单 → 上门 → 打包称重 → 司磅入库 → 质检 → 审批结算
"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login


def login_as(api_session, mobile):
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000))}
    resp = api_session.post(
        f"{ADMIN_URL}/admin-api/system/auth/sms-login",
        json={"mobile": mobile, "code": "9999"}, headers=headers,
    )
    assert resp.status_code == 200 and resp.json()["code"] == 0
    return {"Authorization": f"Bearer {resp.json()['data']['accessToken']}"}


class TestE2EClearChain:
    """清运结算全链路"""

    @pytest.mark.smoke
    def test_e2e_clear(self, api_session):
        station_headers = login_as(api_session, "18600000000")
        driver_headers = login_as(api_session, "18600000001")
        weigher_headers = login_as(api_session, "18600000003")
        inspector_headers = login_as(api_session, "18600000004")
        manager_headers = login_as(api_session, "18600000005")

        # ──────────────────────────────────────────
        # Step 1: 站点呼叫清运
        # ──────────────────────────────────────────
        print("\n[Step 1] 站点呼叫清运...")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/order/call-clean-now",
            json={"stationId": 1, "clearType": 1},  # TODO: 替换实际站点ID
            headers=station_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        clear_id = resp.json()["data"].get("id") or resp.json()["data"]
        print(f"  ✅ 呼单成功 clear_id={clear_id}")

        # ──────────────────────────────────────────
        # Step 2: 司机接单
        # ──────────────────────────────────────────
        print("\n[Step 2] 司机接单...")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/clear-order/driver/accept",
            json={"orderId": clear_id},
            headers=driver_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 司机接单成功")

        # ──────────────────────────────────────────
        # Step 3: 司机出发
        # ──────────────────────────────────────────
        print("\n[Step 3] 司机出发...")
        resp = api_session.put(
            f"{APP_URL}/app-api/recycle/clear-order/driver/depart",
            json={"orderId": clear_id},
            headers=driver_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 司机出发")

        # ──────────────────────────────────────────
        # Step 4: 司机到达站点
        # ──────────────────────────────────────────
        print("\n[Step 4] 司机到达...")
        resp = api_session.put(
            f"{APP_URL}/app-api/recycle/clear-order/driver/arrive",
            json={"orderId": clear_id},
            headers=driver_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 司机到达")

        # ──────────────────────────────────────────
        # Step 5: 打包称重
        # ──────────────────────────────────────────
        print("\n[Step 5] 打包称重...")
        parcel_code = f"P{int(time.time())}"
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/clear-order/driver/weighing-complete",
            json={
                "orderId": clear_id,
                "parcelCode": parcel_code,
                "weight": 50000,  # 50kg
                "productType": 1,
            },
            headers=driver_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 称重完成 parcel={parcel_code} weight=50000g")

        # ──────────────────────────────────────────
        # Step 6: 装车完成
        # ──────────────────────────────────────────
        print("\n[Step 6] 装车完成...")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/clear-order/driver/loading-complete",
            json={"orderId": clear_id},
            headers=driver_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 装车完成 → 待到仓")

        # ──────────────────────────────────────────
        # Step 7: 司磅整车入库
        # ──────────────────────────────────────────
        print("\n[Step 7] 司磅入库...")
        resp = api_session.post(
            f"{ADMIN_URL}/admin-api/recycle/clear-order-weigher/stockin-fullvehicle",
            json={
                "orderId": clear_id,
                "grossWeight": 52000,   # 毛重 52kg
                "tareWeight": 2000,     # 皮重 2kg
                "warehouseId": 1,       # TODO: 替换实际库位ID
            },
            headers=weigher_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 入库成功 净重=50000g")

        # ──────────────────────────────────────────
        # Step 8: 质检员扫码质检
        # ──────────────────────────────────────────
        print("\n[Step 8] 质检员扫码质检...")
        resp = api_session.post(
            f"{APP_URL}/admin-api/recycle/app-operation-center/inspect-one-package",
            json={
                "parcelCode": parcel_code,
                "inspectResult": 1,     # 1=合格
                "inspectWeight": 50000,
                "settlePrice": 100,     # 1元/kg
            },
            headers=inspector_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 质检完成")

        # ──────────────────────────────────────────
        # Step 9: 质检主管审批通过
        # ──────────────────────────────────────────
        print("\n[Step 9] 质检主管审批...")
        resp = api_session.post(
            f"{ADMIN_URL}/admin-api/recycle/app-operation-center/manager-inspect",
            json={
                "orderId": clear_id,
                "auditStatus": 1,  # 1=通过
            },
            headers=manager_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 审批通过 → 结算完成")

        print(f"\n🎉 清运结算全链路通过! clear_id={clear_id}")
