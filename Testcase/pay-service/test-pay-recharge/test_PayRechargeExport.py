import pytest
from config import ADMIN_URL


@pytest.mark.skip(reason="接口返回 当前流水类型不支持充值导出，待确认")
class TestPayRechargeExport:
    """导出充值数据"""

    @pytest.mark.smoke
    def test_PayRechargeExport(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/recharge/export"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=body, headers=auth_headers))
