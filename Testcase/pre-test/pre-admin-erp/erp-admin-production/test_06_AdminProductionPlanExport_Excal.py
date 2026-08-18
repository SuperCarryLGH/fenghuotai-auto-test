import pytest
from config import ADMIN_URL
@pytest.mark.smoke
def test_AdminProductionPlanExport_Excel(api_session,auth_headers):
    body = {
        "pageNo":1,
        "pageSize":10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-plan/export-excel",params=body,headers=auth_headers)
    assert resp.status_code == 200
    print(f"生产计划导出成功")