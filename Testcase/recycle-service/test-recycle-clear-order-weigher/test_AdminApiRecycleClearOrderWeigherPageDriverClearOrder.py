import pytest
from config import ADMIN_URL
from Common.recycle_utils import RecycleChain


class Test_AdminApiRecycleClearOrderWeigherPageDriverClearOrder:
    """称重员司机清运单分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherPageDriverClearOrder(self, weigher_ctx):
        chain, wt = weigher_ctx
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/page-driver-clear-order",
                       {"driverId": RecycleChain.DRIVER_ID, "pageNo": 1, "pageSize": 10},
                       chain._b_headers(wt))
        print(r)
