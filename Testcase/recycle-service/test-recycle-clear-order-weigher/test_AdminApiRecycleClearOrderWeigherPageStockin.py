import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleClearOrderWeigherPageStockin:
    """称重员入库分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherPageStockin(self, weigher_ctx):
        chain, wt = weigher_ctx
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/page-stockin",
                       {"pageNo": 1, "pageSize": 10}, chain._b_headers(wt))
        print(r)
