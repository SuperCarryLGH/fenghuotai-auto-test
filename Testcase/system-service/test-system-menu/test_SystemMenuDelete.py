import pytest
from config import ADMIN_URL


class TestSystemMenuDelete:
    """删除菜单"""

    @pytest.mark.smoke
    def test_SystemMenuDelete(self, api_session, auth_headers, system_menu_id):
        url = f"{ADMIN_URL}/admin-api/system/menu/delete"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        # resp = api_session.delete(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
