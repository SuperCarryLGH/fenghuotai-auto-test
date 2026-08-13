"""recycle-service 共享 fixture：清运链路自建"""
import pytest
from config import ADMIN_URL
from Common.recycle_utils import RecycleChain


@pytest.fixture(scope="function")
def clear_chain(api_session):
    """构建完整清运链路（用户下单→接单→称重→支付→呼叫清运）

    返回 (RecycleChain, clear_order_id, driver_token, station_token)
    测试结束后删除清运单，避免 isCleanInitiated 阻塞后续用例。
    """
    chain = RecycleChain(api_session)
    co_id, order_id, station_token, driver_token, _ = chain.build_chain()
    yield chain, co_id, driver_token, station_token

    try:
        admin_token = chain.login.admin_login("admin")
        api_session.delete(
            f"{ADMIN_URL}/admin-api/recycle/clear-order/delete",
            params={"id": co_id},
            headers={"tenant-id": "1", "appId": "admin", "sign": "admin",
                     "Authorization": f"Bearer {admin_token}"},
        )
    except Exception as e:
        print(f"[cleanup] 删除清运单 {co_id} 失败: {e}")


@pytest.fixture(scope="function")
def order_chain(api_session):
    """构建订单阶段：用户下单（未接单），每次用随机手机号避免防重提交

    返回 (RecycleChain, order_id, station_token, user_token)
    """
    import time as _t
    chain = RecycleChain(api_session)
    mobile = "156" + str(int(_t.time() * 1000))[-8:]
    user_token = chain.login.app_login_with(mobile=mobile, code="9999")
    station_token = chain.station_login()
    order_id = chain.create_order(user_token, user_mobile=mobile)
    yield chain, order_id, station_token, user_token


@pytest.fixture(scope="function")
def weigher_ctx(api_session):
    """称重员 B端 上下文"""
    chain = RecycleChain(api_session)
    wt = chain.weigher_login()
    yield chain, wt


@pytest.fixture(scope="function")
def clue_chain(api_session, auth_headers):
    """创建站点线索 → yield (RecycleChain, clue_id, clue_no, auth_headers)"""
    chain = RecycleChain(api_session)
    clue_id, clue_no = chain.create_clue(auth_headers)
    yield chain, clue_id, clue_no, auth_headers

    try:
        api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station-clue/delete",
                           params={"id": clue_id}, headers=auth_headers)
    except Exception as e:
        print(f"[cleanup] 删除线索 {clue_id} 失败: {e}")
