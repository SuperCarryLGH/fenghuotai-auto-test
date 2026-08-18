import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundExportExcel(api_session, auth_headers):
    """导出竞拍场次 Excel"""
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-round/export-excel",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    assert "application/vnd.ms-excel" in resp.headers.get("Content-Type", ""), \
        f"竞拍场次导出响应类型异常: {resp.headers.get('Content-Type')}"
    print(f"竞拍场次导出成功，文件大小：{len(resp.content)} bytes")
