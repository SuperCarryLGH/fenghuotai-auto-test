import pytest
from config import APP_URL


class Teststation_order_submit:
    """"""

    @pytest.mark.smoke
    def test_station_order_submit(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/order/station-order-submit"
        params = {"id": "order_flow_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
