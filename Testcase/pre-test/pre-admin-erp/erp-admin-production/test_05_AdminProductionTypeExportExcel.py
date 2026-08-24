import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionTypeExport_Excel(api_session, auth_headers):
    """导出生产类型 Excel"""
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-type/export-excel",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.content) > 0
    print(f"生产类型导出成功，文件大小：{len(resp.content)} bytes")
