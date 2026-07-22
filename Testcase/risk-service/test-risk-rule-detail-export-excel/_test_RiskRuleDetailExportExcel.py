import pytest
from config import ADMIN_URL


class TestRiskRuleDetailExportExcel:
    """导出风控-规则区间明细 Excel"""

    @pytest.mark.smoke
    def test_RiskRuleDetailExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/export-excel"
        params = {
            "pageNo":1,
            "pageSize":10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        # 导出接口返回二进制 Excel，不解析 JSON
        content_type = resp.headers.get("Content-Type", "")
        assert len(resp.content) > 0
        print(f"下载成功, 文件大小={len(resp.content)}bytes, Content-Type={content_type}")
