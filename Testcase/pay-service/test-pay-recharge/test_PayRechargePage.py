import pytest
from config import ADMIN_URL


class TestPayRechargePage:
    """获得充值分页"""

    @pytest.mark.smoke
    def test_PayRechargePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/recharge/page"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        # resp = api_session.get(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
