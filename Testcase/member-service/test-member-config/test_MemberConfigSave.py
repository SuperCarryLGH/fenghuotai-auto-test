import pytest
from config import ADMIN_URL


class TestMemberConfigSave:
    """保存会员配置"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="会修改真实会员配置(id=1)，暂不执行")
    def test_MemberConfigSave(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/config/save"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": 1}  # TODO: 补充参数
        # resp = api_session.put(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
