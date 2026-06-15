import pytest
from config import ADMIN_URL
from Common.loader import load_yaml, DATA_DIR
import os
import yaml
from Common.loader import load_member_tag_create
create = load_member_tag_create()


class TestMemberTagCreate:
    """创建会员标签"""

    @pytest.mark.smoke
    def test_MemberTagCreate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        new_ids = []
        url = f"{ADMIN_URL}/admin-api/member/tag/create"
        params = {
            "name": create["create"]["name"]
            }
        resp = api_session.post(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        new_id = r["data"]

        # 使用 yaml 库操作文件
        yaml_path = os.path.join(DATA_DIR, "member_tag_delete.yaml")

        # 读取现有YAML
        with open(yaml_path, encoding="utf-8") as f:
            delete_data = yaml.safe_load(f)

        # 更新ID
        delete_data['delete']['id'] = new_id

        # 写回文件
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(delete_data, f, allow_unicode=True, default_flow_style=False)
        assert r["code"] == 0
        #assert r["data"] == {}
        print(f"创建的标签ID: {new_id}")
        print(r)








#test_AppApiCooperationGetByPlatform