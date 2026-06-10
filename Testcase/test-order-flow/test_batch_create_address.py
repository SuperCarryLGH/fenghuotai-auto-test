import os
import pytest
from config import APP_URL
from Common.loader import load_yaml, DATA_DIR
from Common.login import Login


class TestBatchCreateAddress:
    """批量创建用户地址 — 每个用户用自己的 token 创建自己的地址"""

    @pytest.mark.smoke
    def test_batch_create_address(self, api_session, login_tool):
        data = load_yaml("batch_users.yaml")
        users = data["batch_users"]

        new_ids = []

        for user in users:
            token = login_tool.app_login(mobile=user["mobile"])
            headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
            payload = user["address"].copy()
            payload.pop("addressId", None)

            resp = api_session.post(
                f"{APP_URL}/app-api/member/address/create",
                json=payload,
                headers=headers,
            )
            assert resp.status_code == 200
            resp_data = resp.json()
            assert resp_data["code"] == 0
            address_id = resp_data["data"]
            new_ids.append(address_id)

        yaml_path = os.path.join(DATA_DIR, "batch_users.yaml")
        with open(yaml_path, encoding="utf-8") as f:
            text = f.read()

        for aid in new_ids:
            text = text.replace('addressId: ""', f'addressId: "{aid}"', 1)

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(text)
