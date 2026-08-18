import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionTypeExport_Excel(api_session, auth_headers):
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-type/export-excel",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    assert "application/vnd.ms-excel" in resp.headers.get("Content-Type", ""), \
        f"生产类型导出响应类型异常: {resp.headers.get('Content-Type')}"
    print(f"生产类型导出成功，文件大小：{len(resp.content)} bytes")
