import pytest
from config import APP_URL
class TestDistPromoterSignAgreement:
    """运营协议签署（done）"""
    URL = f"{APP_URL}/app-api/dist/promoter/sign-agreement"
    date = {"agreementUrl": "https://example.com/agreement/signed_123.pdf"}
    @pytest.mark.smoke
    def test_DistPromoterSignAgreement(self, api_session, promoterinfo_headers,ok):
        r=ok(api_session.post(self.URL, json=self.date,headers=promoterinfo_headers))
        print(r)