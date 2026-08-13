import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleClearOrderWeigherDashboard:
    """称重员仪表盘"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherDashboard(self, weigher_ctx):
        chain, wt = weigher_ctx
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/dashboard",
                       {}, chain._b_headers(wt))
        print(r)
