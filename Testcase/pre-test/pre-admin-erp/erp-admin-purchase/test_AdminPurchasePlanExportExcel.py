import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanExportExcel(api_session, auth_headers):
    """导出采购计划 Excel"""
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-plan/export-excel",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.content) > 0
    print(f"采购计划导出成功，文件大小：{len(resp.content)} bytes")
