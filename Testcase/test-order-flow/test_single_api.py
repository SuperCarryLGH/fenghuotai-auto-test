import time
import pytest
from config import ADMIN_URL
from Common.loader import load_users, load_common
users = load_users()
common = load_common()


class TestUserApi:
    """管理后台 - 用户模块单接口测试"""

    @pytest.mark.smoke
    def test_get_user_detail(self, api_session, auth_headers):
        """获取用户详情"""
        url = f"{ADMIN_URL}/admin-api/system/user/get"
        params = {"id": users["users"]["normal_user"]["id"]}

        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        # 后续断言从响应里取具体字段
        # assert r["data"]["username"] == "xxx"

    @pytest.mark.smoke
    def test_role_page(self, api_session, auth_headers):
        """角色分页查询"""
        url = f"{ADMIN_URL}/admin-api/system/role/page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}

        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0

    @pytest.mark.smoke
    def test_create_role(self, api_session, auth_headers):
        """创建角色"""
        url = f"{ADMIN_URL}/admin-api/system/role/create"
        suffix = str(int(time.time()))
        body = {"name": f"测试角色_{suffix}", "code": f"TEST_ROLE_{suffix}", "status": common['common']['status']['enabled'], "sort": 1}

        resp = api_session.post(url, json=body, headers=auth_headers)

        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
