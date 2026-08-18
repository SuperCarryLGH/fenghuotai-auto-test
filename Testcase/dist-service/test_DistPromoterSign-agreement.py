import pytest
from config import APP_URL
class TestDistPromoterSignAgreement:
    """运营协议签署：动态推广员已签约，重复签约应被拒绝"""
    URL = f"{APP_URL}/app-api/dist/promoter/sign-agreement"
    date = {"agreementUrl": "https://example.com/agreement/signed_123.pdf"}

    @pytest.mark.smoke
    def test_DistPromoterSignAgreement(self, api_session, autotest_promoter_headers, ok):
        r = api_session.post(self.URL, json=self.date, headers=autotest_promoter_headers)
        assert r.status_code == 200
        data = r.json()
        # 动态推广员已签约，再次签约应被拒绝（code=10023 推广员已签署协议）
        assert data["code"] != 0 and data["code"] != "0", f"重复签约应被拒绝，实际成功: {data}"
        print(f"  重复签约被拒（符合预期）: {data}")