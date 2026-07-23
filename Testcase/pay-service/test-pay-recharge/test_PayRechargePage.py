import pytest
from config import ADMIN_URL


class TestPayRechargePage:
    """获得充值分页"""

    @pytest.mark.smoke
    def test_PayRechargePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/recharge/page"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        ok(api_session.get(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
