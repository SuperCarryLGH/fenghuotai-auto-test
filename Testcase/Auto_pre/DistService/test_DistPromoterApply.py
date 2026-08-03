"""推广达人申请"""
import pytest
from config import APP_URL
from Common.loader import load_yaml


class TestDistPromoterApply:
    URL = f"{APP_URL}/app-api/dist/promoter/apply"
    DATA = load_yaml("promoter_apply.yaml")

    @pytest.mark.smoke
    def test_DistPromoterApply(self, api_session, promoter_headers, ok):
        r = ok(api_session.post(self.URL, json=self.DATA["default"], headers=promoter_headers))
        print(r)

    #def test_apply_no_media(self, api_session, promoter_headers, ok):
        #r = ok(api_session.post(self.URL, json=self.DATA["no_media"], headers=promoter_headers))
        #print(r)
