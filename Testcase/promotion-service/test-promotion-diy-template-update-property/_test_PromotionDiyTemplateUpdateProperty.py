import pytest
from config import ADMIN_URL


class TestPromotionDiyTemplateUpdateProperty:
    """更新装修模板属性"""

    @pytest.mark.smoke
    def test_PromotionDiyTemplateUpdateProperty(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-template/update-property"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
