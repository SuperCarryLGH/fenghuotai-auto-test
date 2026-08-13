"""独立调试：按团长手机号解析团队，批量提交成员入团申请（不审核、不绑定上级）

用法:
    cd /Users/rs/PycharmProjects/PythonProject1
    .venv/bin/python3 Testcase/Auto_pre/DistService/debug_join_team.py

说明:
    - 团长手机号需已是团长（已有团队）
    - 成员只提交入团申请（状态=待审核），不自动审核、不绑定上级
    - dev 环境免验证码(9999)；MANUAL_CODE=True 时逐个手动输入
"""
import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import requests
from functools import partial

from Common.team_utils import TeamUtils
from Common.login import Login
from Common.DB import DBClient
from config import APP_URL

# ==================== 配置区 ====================
LEADER_MOBILE = "15600000001"                  # ← 团长手机号（需已是团长）
MEMBERS = ["15600000002", "15600000003"]       # ← 要入团的成员手机号（手动填写）
MANUAL_CODE = False                            # True=手动输验证码（线上用）
# ===============================================


def _login(lt, mobile):
    """登录；MANUAL_CODE=True 时先发短信再手动输入"""
    if MANUAL_CODE:
        lt.send_sms_code(mobile)
        code = input(f"请输入 {mobile} 收到的验证码: ").strip()
        return lt.app_login_for_promoter(mobile=mobile, code=code)
    return lt.app_login_for_promoter(mobile=mobile)


def main():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 Chrome/120",
    })
    s.request = partial(s.request, timeout=10)
    lt = Login(session=s)
    db = DBClient()
    admin_token = lt.admin_login("admin")
    tu = TeamUtils(s, lt, db, admin_token)

    print(f"\n===== 团长解析: {LEADER_MOBILE} =====")
    token_leader = _login(lt, LEADER_MOBILE)
    info = tu.get_promoter_info(token_leader)
    team_info = info.get("teamInfo") or {}
    team_id = team_info.get("teamId")
    if not team_id or int(team_id) <= 0:
        print(f"  ❌ 团长 {LEADER_MOBILE} 没有团队，无法解析 team_id")
        db.close()
        return
    team_id = int(team_id)
    print(f"  团长 {LEADER_MOBILE}: promoter_id={info.get('promoterId')}, "
          f"团队 team_id={team_id}, team_name={team_info.get('teamName')}")
    row = db.fetch_one("SELECT team_name FROM dist_team WHERE id=%s AND deleted=0", (team_id,))
    if row:
        print(f"  DB 确认团队: team_id={team_id}, team_name={row['team_name']}")

    print(f"\n===== 批量提交入团申请（{len(MEMBERS)} 人） =====")
    results = []
    for i, mb in enumerate(MEMBERS):
        try:
            _, apply_id = tu.join_team(mb, team_id)
            pid = tu.get_promoter_id_by_mobile(mb)
            results.append({"mobile": mb, "pid": pid, "apply_id": apply_id, "ok": True})
            print(f"  [{i+1}/{len(MEMBERS)}] 成员 {mb}: promoter_id={pid}, "
                  f"入团申请 apply_id={apply_id}, 状态=待审核")
        except Exception as e:
            results.append({"mobile": mb, "ok": False, "err": str(e)})
            print(f"  [{i+1}/{len(MEMBERS)}] 成员 {mb}: 申请失败 - {e}")

    print(f"\n===== 汇总 =====")
    ok = [r for r in results if r["ok"]]
    fail = [r for r in results if not r["ok"]]
    print(f"  成功提交申请 {len(ok)} 人，失败 {len(fail)} 人")
    for r in fail:
        print(f"   ❌ {r['mobile']}: {r['err']}")
    print("  申请均为【待审核】，需团长在 APP/后台审核后正式入团")
    db.close()


if __name__ == "__main__":
    main()
