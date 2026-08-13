import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleClearOrderWeigherPageArrivedDriver:
    """称重员已到达司机分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherPageArrivedDriver(self, weigher_ctx):
        chain, wt = weigher_ctx
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/page-arrived-driver",
                       {"pageNo": 1, "pageSize": 10}, chain._b_headers(wt))
        print(r)
