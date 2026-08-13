import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherGetStockinDetail:
    """称重员获取入库详情"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="后端 loading-complete 自动结算导致清运单无法执行入库，待后端确认")
    def test_AdminApiRecycleClearOrderWeigherGetStockinDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/get-stockin-detail"
        params = {"inId": weigher_data['weigher']['order_id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
