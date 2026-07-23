import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherGetStockinDetail:
    """称重员获取入库详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherGetStockinDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/get-stockin-detail"
        params = {"id": weigher_data['weigher']['order_id']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
