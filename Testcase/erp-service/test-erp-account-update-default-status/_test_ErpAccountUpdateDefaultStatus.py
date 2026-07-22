import pytest
from config import ADMIN_URL


class TestErpAccountUpdateDefaultStatus:
    """更新结算账户默认状态"""

    @pytest.mark.smoke
    def test_ErpAccountUpdateDefaultStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/account/update-default-status"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
