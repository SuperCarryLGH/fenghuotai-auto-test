import pytest
from config import APP_URL


class TestDistPromoterRank:
    """推广员拉新排行榜"""
    URL = f"{APP_URL}/app-api/dist/promoter/rank"
    @pytest.mark.smoke
    def test_DistPromoterRank(self, api_session, promoter_headers,ok):
        r=ok(api_session.get(self.URL, headers=promoter_headers))
        print(r)