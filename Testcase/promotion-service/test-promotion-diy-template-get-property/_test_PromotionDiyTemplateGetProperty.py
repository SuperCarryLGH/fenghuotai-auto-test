import pytest
from config import ADMIN_URL


class TestPromotionDiyTemplateGetProperty:
    """获得装修模板属性"""

    @pytest.mark.smoke
    def test_PromotionDiyTemplateGetProperty(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-template/get-property"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
