import pytest
from config import ADMIN_BASE_URL, ENV


class TestUserApi:
    """管理后台 - 用户模块单接口测试"""

    @pytest.mark.smoke
    def test_get_user_detail(self, api_session, auth_headers):
        """获取用户详情"""
        url = f"{ADMIN_BASE_URL[ENV]}/system/user/get"
        params = {"id": "USER_ID_NORMAL_001"}

        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        # 后续断言从响应里取具体字段
        # assert data["data"]["username"] == "xxx"

    @pytest.mark.smoke
    def test_role_page(self, api_session, auth_headers):
        """角色分页查询"""
        url = f"{ADMIN_BASE_URL[ENV]}/system/role/page"
        params = {"pageNo": 1, "pageSize": 10}

        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0

    @pytest.mark.smoke
    def test_create_role(self, api_session, auth_headers):
        """创建角色"""
        url = f"{ADMIN_BASE_URL[ENV]}/system/role/create"
        body = {"name": "测试角色_todo", "code": "TEST_ROLE"}

        resp = api_session.post(url, json=body, headers=auth_headers)

        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
