import pytest
from config import APP_URL
from Common.loader import load_yaml
class TestDistPromoterRealNameAuth:
    """推广员实名认证"""
    URL = f"{APP_URL}/app-api/dist/promoter/real-name-auth"
    date = load_yaml("RealNameAuth.yaml")
    @pytest.mark.smoke
    def test_DistPromoterMyPromoteStats(self, api_session, promoterinfo_headers,ok):
        r=(api_session.post(self.URL, json=self.date['auth_msg'],headers=promoterinfo_headers))
        print(r)