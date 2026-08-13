"""
调试工具：单个上级 + N 个邀请人 的星型拉新链路

用法：
  1. 在下方配置区填写 BASE_MOBILE（上级手机号）和 INVITE_NUM（邀请人数）
  2. cd PycharmProjects/PythonProject1
  3. .venv/bin/python3 Testcase/Auto_pre/test-preDist/debug_invite_flow.py

流程：
  - 校验上级是否已为推广官：已注册则复用，未注册则完整注册
  - 生成 INVITE_NUM 个邀请人，全部绑定到该上级下并完整注册推广官
  - 每个邀请人各自下单 → 检查上级拉新奖励（source_type=10）与余额变化
"""

import os
import sys

# 自动将项目根目录加入 path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_script_dir, "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import time
import warnings
warnings.filterwarnings("ignore")
import requests

from Common.team_utils import TeamUtils
from Common.login import Login
from Common.DB import DBClient
from config import APP_URL

# =========================================
# 配置区域（在此填写）
# =========================================
BASE_MOBILE = "15605842344"        # ← 上级手机号（在此填写）
INVITE_NUM = 5          # ← 邀请人数（在此填写）
ORDER_NUM = 1          # 每单回收数量
PREDICT_WEIGHT = "5~10kg"
WAIT_SECONDS = 3
# =========================================


def p(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


def ensure_promoter(tu, mobile, promoter_id=None):
    """校验是否已为推广官：已存在则复用，未注册则完整注册"""
    token = tu.login.app_login_for_promoter(mobile=mobile,
                                            promoter_id=promoter_id)
    r = tu.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                 headers=tu.app_headers(token), verify=False).json()
    if r.get("code") == 0 and r["data"].get("promoterId"):
        pid = int(r["data"]["promoterId"])
        info = r["data"]
        parent = info.get("parentPromoterId")
        if promoter_id and parent and parent != promoter_id:
            print(f"  ⚠ 已有上级parent_pid={parent} != 期望{promoter_id}")
        print(f"  ✅ 已注册推广官: pid={pid}, parent_pid={parent}, "
              f"level={info.get('level')}, star={info.get('star')}, "
              f"余额={info.get('commissionBalance')}分")
        return pid, token
    print("  ➡ 未注册推广官，执行完整注册...")
    return tu.become_promoter(mobile, promoter_id=promoter_id)


def dump_records(db, account_id, account_type, label):
    rows = db.fetch_all(
        "SELECT r.id, r.price, r.order_id, r.source_type, r.status, "
        "r.create_time, r.income_target_type "
        "FROM dist_commission_record r "
        "JOIN dist_commission_account a ON r.commission_account_id = a.id "
        "WHERE a.account_id=%s AND a.account_type=%s "
        "AND r.deleted=0 AND a.deleted=0 "
        "ORDER BY r.create_time DESC",
        (account_id, account_type))
    total = sum(float(r["price"]) for r in rows) if rows else 0
    print(f"  {label}: account_id={account_id} type={account_type} "
          f"共{len(rows)}条 合计={total}分")
    for r in rows:
        print(f"    id={r['id']} price={r['price']} order_id={r['order_id']} "
              f"source={r['source_type']} target={r['income_target_type']} "
              f"status={r['status']} {r['create_time']}")
    return total


if __name__ == "__main__":
    assert BASE_MOBILE, "请在配置区填写 BASE_MOBILE（上级手机号）"
    assert INVITE_NUM > 0, "INVITE_NUM（邀请人数）需大于0"
    p(f"星型拉新调试: 上级={BASE_MOBILE} 邀请人数={INVITE_NUM}")

    s = requests.Session()
    s.verify = False
    s.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0",
    })
    login_tool = Login(session=s)
    admin_token = login_tool.admin_login("admin")
    db = DBClient()
    tu = TeamUtils(s, login_tool, db, admin_token)

    # 1. 上级校验/注册
    p(f"上级 {BASE_MOBILE} 校验")
    pid_a, token_a = ensure_promoter(tu, BASE_MOBILE)

    # 2. 拉新配置
    info_a = tu.get_promoter_info(token_a)
    cfg = tu.get_invite_config(info_a["level"], info_a["star"],
                               rule_type=1, token=token_a)
    first_reward = int(cfg["first_invite_reward"])
    print(f"  一级拉新奖励={first_reward}分, 二级拉新奖励={cfg['second_invite_reward']}分")
    print(f"  first_team_rate={cfg['first_invite_team_reward_rate']} "
          f"second_team_rate={cfg['second_invite_team_reward_rate']}")

    # 3. 记录上级下单前状态
    reward_before = tu.get_invite_reward_sum(pid_a, account_type=1)
    balance_before = info_a["commissionBalance"]
    print(f"  拉新奖励sum(前)={reward_before}分, 余额(前)={balance_before}分")

    # 4. 生成邀请人并注册+绑定上级+各自下单
    p(f"生成 {INVITE_NUM} 个邀请人，绑定 {BASE_MOBILE} 并下单")
    invitees = []
    for i in range(INVITE_NUM):
        mb = TeamUtils.gen_mobile()
        pid_i, token_i = ensure_promoter(tu, mb, promoter_id=pid_a)
        oid = tu.settle_order(token_i, mb, num=ORDER_NUM,
                              predict_weight=PREDICT_WEIGHT)
        invitees.append({"mobile": mb, "pid": pid_i, "order_id": oid})
        print(f"  [{i+1}/{INVITE_NUM}] 邀请人{mb} pid={pid_i} "
              f"订单{oid} 下单完成")

    # 5. 等待入账
    p(f"等待 {WAIT_SECONDS}s 入账...")
    for i in range(WAIT_SECONDS):
        time.sleep(1)
        print(f"  {i+1}s", end="")
    print()

    # 6. 上级拉新奖励校验
    p("上级拉新奖励")
    reward_after = tu.get_invite_reward_sum(pid_a, account_type=1)
    expected_reward = reward_before + first_reward * INVITE_NUM
    diff_reward = reward_after - reward_before
    ok = "✅" if diff_reward == first_reward * INVITE_NUM else "❌"
    print(f"  {ok} 拉新奖励: 预期+{first_reward*INVITE_NUM}分, "
          f"实际+{diff_reward}分 (sum {reward_before}→{reward_after})")

    # 7. 余额变化（含下单佣金）
    info_a2 = tu.get_promoter_info(token_a)
    balance_after = info_a2["commissionBalance"]
    bal_diff = balance_after - balance_before
    print(f"  余额: {balance_before}→{balance_after}({bal_diff:+d}分) "
          f"[拉新{diff_reward} + 佣金{bal_diff-diff_reward}]")

    # 8. 订单信息
    p("各邀请人订单")
    for i, inv in enumerate(invitees):
        row = tu.db.fetch_one(
            "SELECT real_weight, total_price FROM recycle_order "
            "WHERE id=%s AND deleted=0", (inv["order_id"],))
        w = row["real_weight"] if row else "?"
        pr = row["total_price"] if row else "?"
        print(f"  邀请人[{i+1}] {inv['mobile']} pid={inv['pid']} "
              f"订单{inv['order_id']} weight={w} price={pr}")

    # 9. DB 全量记录
    p("上级佣金账户记录")
    dump_records(db, pid_a, 1, f"上级({BASE_MOBILE})")

    p("各邀请人佣金账户记录")
    for i, inv in enumerate(invitees):
        dump_records(db, inv["pid"], 1, f"邀请人[{i+1}]")

    p("调试完成")
