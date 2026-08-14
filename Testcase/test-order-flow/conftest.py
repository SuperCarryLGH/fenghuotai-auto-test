import time

import pytest

from Common.skywalking import SkyWalking


@pytest.fixture
def sw_trace():
    """SkyWalking 链路工具：返回 (sw, now_ms, locate)。

    用法:
        sw, now_ms, locate = sw_trace()
        t0 = now_ms()
        r = ok(api_session.post(url, json=payload, headers=headers))
        trace_id = locate(endpoint="POST:/recycle/order/v2/mini-order-submit", t0=t0)
        if trace_id:
            logs = sw.query_logs(trace_id=trace_id, keyword="Exception")
    """
    sw = SkyWalking()

    def now_ms():
        return int(time.time() * 1000)

    def locate(endpoint, t0):
        trace_id = sw.locate_latest(endpoint=endpoint, t0=t0)
        if trace_id:
            sw.locate(trace_id)
        else:
            print(f"[SkyWalking] {endpoint} 未定位到链路")
        return trace_id

    return sw, now_ms, locate
