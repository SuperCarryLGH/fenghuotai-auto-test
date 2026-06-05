import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherScanStockin:
    """称重员扫码入库"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherScanStockin(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/weigher/scan-stockin"
        body = {"id": weigher_data['weigher']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
