import os
import re
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

        new_ids = [None] * len(users)
        failures = []

        for i, user in enumerate(users):
            desc = user.get("desc", user["mobile"])
            try:
                token = login_tool.app_login(mobile=user["mobile"])
                headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
                payload = user["address"].copy()
                payload.pop("addressId", None)

                resp = api_session.post(
                    f"{APP_URL}/app-api/member/address/create",
                    json=payload,
                    headers=headers,
                )
                resp_data = resp.json()
                assert resp.status_code == 200, f"HTTP {resp.status_code}"
                assert resp_data["code"] == 0, f"code={resp_data['code']}, msg={resp_data.get('msg', '')}"
                address_id = resp_data["data"]
                new_ids[i] = address_id
                print(f"✅ {desc} → {address_id}")
            except Exception as e:
                failures.append((desc, str(e)))
                print(f"❌ {desc} → {e}")

        yaml_path = os.path.join(DATA_DIR, "batch_users.yaml")
        with open(yaml_path, encoding="utf-8") as f:
            text = f.read()

        idx = 0
        def _replace(m):
            nonlocal idx
            val = new_ids[idx]
            idx += 1
            if val is not None:
                return f'addressId: "{val}"'
            return m.group(0)

        text = re.sub(r'addressId:\s*".*"', _replace, text)

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(text)

        if failures:
            msg = "\n".join(f"  {d}: {e}" for d, e in failures)
            pytest.fail(f"以下地址创建失败:\n{msg}")
