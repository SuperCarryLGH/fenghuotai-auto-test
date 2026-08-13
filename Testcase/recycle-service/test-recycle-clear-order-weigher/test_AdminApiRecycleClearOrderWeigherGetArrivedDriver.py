import pytest
from config import ADMIN_URL
from Common.recycle_utils import RecycleChain


class Test_AdminApiRecycleClearOrderWeigherGetArrivedDriver:
    """称重员获取已到达司机"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherGetArrivedDriver(self, weigher_ctx):
        chain, wt = weigher_ctx
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/get-arrived-driver",
                       {"driverId": RecycleChain.DRIVER_ID}, chain._b_headers(wt))
        print(r)
