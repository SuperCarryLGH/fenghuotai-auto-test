"""独立调试：手机号 + promoterId 登录（手动输入验证码），打印登录结果与绑定关系

用法:
    cd /Users/rs/PycharmProjects/PythonProject1
    .venv/bin/python3 Testcase/Auto_pre/DistService/debug_promoter_login.py

说明: 交互式运行（需手动输入验证码）。dev 环境免验证码时直接输入 9999 即可。
"""
import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import requests
from functools import partial

from Common.login import Login
from Common.DB import DBClient

# ==================== 配置区 ====================
MOBILE = "18900000002"               # ← 要登录的手机号（dev 环境填 dev 测试号）
PROMOTER_ID = 2085291788430340098    # ← 要绑定的上级推广员ID（dev 环境填 dev 的）
CHECK_DB = False                     # 是否查绑定关系(涉及数据库)。线上登录可设为 False
# ===============================================


def main():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 Chrome/120",
    })
    s.request = partial(s.request, timeout=10)
    lt = Login(session=s)
    db = DBClient() if CHECK_DB else None

    # 1. 发送短信验证码
    try:
        ok = lt.send_sms_code(MOBILE)
        print(f"[1] 发送验证码到 {MOBILE}: {'成功' if ok else '失败'}")
    except Exception as e:
        print(f"[1] 发送验证码失败: {e}")

    # 2. 手动输入验证码
    code = input(f"[2] 请输入 {MOBILE} 收到的验证码: ").strip()

    # 3. 带 promoterId 登录
    try:
        token = lt.app_login_for_promoter(mobile=MOBILE, code=code, promoter_id=PROMOTER_ID)
        print(f"[3] 登录成功, token 前20位: {token[:20]}")
    except Exception as e:
        print(f"[3] 登录失败: {e}")
        if db:
            db.close()
        return

    # 4. 查绑定关系（可选，涉及数据库）
    if not db:
        print("[4] CHECK_DB=False，跳过绑定关系查询")
        return
    print("[4] 绑定关系:")
    u = db.fetch_one("SELECT id, mobile FROM member_user WHERE mobile=%s", (MOBILE,))
    if u:
        rels = db.fetch_all(
            "SELECT parent_promoter_id, promoter_id, user_id, bind_source, bind_time "
            "FROM dist_promoter_user_relation "
            "WHERE (parent_promoter_id=%s OR user_id=%s) AND deleted=0",
            (PROMOTER_ID, u["id"]))
        for r in rels or []:
            print("   ", r)
        if not rels:
            print("     无绑定关系记录")
    else:
        print("     未找到该手机号的会员")

    db.close()


if __name__ == "__main__":
    main()
