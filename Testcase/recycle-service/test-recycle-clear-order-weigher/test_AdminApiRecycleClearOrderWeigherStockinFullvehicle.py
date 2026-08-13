import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherStockinFullvehicle:
    """称重员整车入库"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="后端 loading-complete 自动结算导致清运单无法执行入库，待后端确认")
    def test_AdminApiRecycleClearOrderWeigherStockinFullvehicle(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/stockin-fullvehicle"
        body = {"id": weigher_data['weigher']['order_id']}
        ok(api_session.post(url, json=body, headers=auth_headers))
