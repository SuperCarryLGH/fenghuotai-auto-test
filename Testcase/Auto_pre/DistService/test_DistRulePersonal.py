import pytest
from config import APP_URL


class TestDistRulePersonal:
    """获得个人分销规则"""
    URL = f"{APP_URL}/app-api/dist/rule/get"
    @pytest.mark.smoke
    def test_DistRulePersonal(self, api_session, rulepersonal_headers,ok):
        r=ok(api_session.get(self.URL, params={"promoteType": 10}, headers=rulepersonal_headers))
        print(r)