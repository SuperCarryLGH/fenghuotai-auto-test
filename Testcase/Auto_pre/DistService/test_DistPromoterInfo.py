import pytest
from config import APP_URL


class TestDistPromoterInfo:
    """获取推广员信息"""
    URL = f"{APP_URL}/app-api/dist/promoter/info"
    @pytest.mark.smoke
    def test_DistPromoterInfo(self, api_session, promoterinfo_headers,ok):
        r=ok(api_session.get(self.URL, headers=promoterinfo_headers))
        print(r)