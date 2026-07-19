import pytest
from config import ADMIN_URL


class TestPayWithdrawAudit:
    """审核提现申请"""

    @pytest.mark.smoke
    def test_PayWithdrawAudit(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/withdraw/audit"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": 1}  # TODO: 补充参数
        # resp = api_session.put(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
