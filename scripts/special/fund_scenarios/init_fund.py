"""
资金初始化 v7 — 统计报告 + SQL 生成
cd /Users/rs/PycharmProjects/PythonProject1 && source .venv/bin/activate && python Testcase/special/fund_scenarios/init_fund.py
只跑常州的话改 SC_FILTER = ["常州分拣中心"]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

DATA_SRC = "/Users/rs/Documents"
OUTPUT_SQL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "Date", "init_fund.sql")
TENANT_ID = 1

# 按分拣中心筛选生成（留空生成全部；示例：["常州分拣中心"]）
SC_FILTER = []

def _to_int(v):
    """字符串→int，保留大数字精度，兼容小数如'7.28'"""
    if v is None or (isinstance(v, float) and pd.isna(v)): return 0
    s = str(v).strip()
    if not s or s == 'nan': return 0
    if '.' in s: return int(float(s))
    return int(s)

stations      = pd.read_excel(f"{DATA_SRC}/station.xlsx", dtype={"id": str, "virtual_user_id": str, "company_id": str})
wallets       = pd.read_excel(f"{DATA_SRC}/pay_wallet.xlsx", dtype={"id": str, "user_id": str})
trans         = pd.read_excel(f"{DATA_SRC}/pay_wallet_transaction.xlsx", dtype={"id": str, "wallet_id": str, "biz_id": str})
recycle_orders = pd.read_excel(f"{DATA_SRC}/recycle_order.xlsx", dtype={"id": str, "user_id": str, "operation_center_id": str})
withdraws     = pd.read_excel(f"{DATA_SRC}/pay_withdraw.xlsx", dtype={"id": str, "user_id": str})
system_users  = pd.read_excel(f"{DATA_SRC}/system_users.xlsx", dtype=str) if os.path.exists(f"{DATA_SRC}/system_users.xlsx") else None
member_users = pd.read_excel(f"{DATA_SRC}/member_user.xlsx", dtype={"id": str, "operation_center_id": str})
pay_fund_df  = pd.read_excel(f"{DATA_SRC}/pay_fund.xlsx", dtype={"id": str, "org_id": str})

# system_users ID 集合 — 用于排除网点人员
sys_uid_set = set()
if system_users is not None:
    col = "id" if "id" in system_users.columns else system_users.columns[0]
    sys_uid_set = set(int(x) for x in system_users[col].dropna() if pd.notna(x))

# 分拣中心列表
sc_df = stations[stations["station_type"] == 10]
sc_name = {int(r["id"]): r["name"] for _, r in sc_df.iterrows()}
sc_company = {int(r["id"]): int(r["company_id"]) if pd.notna(r.get("company_id")) else 0 for _, r in sc_df.iterrows()}
sc_ids = set(sc_name.keys())

# member_user → 分拣中心映射: user_id → operation_center_id
mu_sc = {}
for _, mu in member_users.iterrows():
    uid = int(mu["id"]) if pd.notna(mu.get("id")) else 0
    oc = int(mu.get("operation_center_id", 0)) if pd.notna(mu.get("operation_center_id")) else 0
    if uid and oc in sc_ids:
        mu_sc[uid] = oc

# pay_fund_id 映射: sc_id → pay_fund.id
sc_pay_fund = {}
for _, pf in pay_fund_df.iterrows():
    ft = int(pf["fund_type"]) if pd.notna(pf.get("fund_type")) else 0
    oid = int(pf["org_id"]) if pd.notna(pf.get("org_id")) else 0
    if ft == 20 and oid: sc_pay_fund[oid] = int(pf["id"])

# SC 基金基线 (pay_fund 当前值)
sc_baseline_total = {}; sc_baseline_wechat = {}; sc_baseline_alipay = {}
for _, pf in pay_fund_df.iterrows():
    ft = int(pf["fund_type"]) if pd.notna(pf.get("fund_type")) else 0
    oid = int(pf["org_id"]) if pd.notna(pf.get("org_id")) else 0
    if ft == 20 and oid:
        sc_baseline_total[oid] = int(pf["total_fund"]) if pd.notna(pf.get("total_fund")) else 0
        sc_baseline_wechat[oid] = int(pf["wechat_fund"]) if pd.notna(pf.get("wechat_fund")) else 0
        sc_baseline_alipay[oid] = int(pf["alipay_fund"]) if pd.notna(pf.get("alipay_fund")) else 0

# 公司ID集合 (从 sc_company 反推)
comp_ids = set(sc_company.values())

user_sc = {}
completed = recycle_orders[
    recycle_orders["status"].notna() & (recycle_orders["status"] == 30)
].sort_values("create_time")
for _, ro in completed.iterrows():
    try:
        uid = _to_int(ro["user_id"])
        oc = _to_int(ro["operation_center_id"])
    except: continue
    if uid and oc in sc_ids and uid not in user_sc:
        user_sc[uid] = oc

# provider 降级映射: user_id → SC id (仅对 mu_sc/user_sc 未覆盖的用户)
SC_CHANGZHOU = 2071977701136384001
SC_WENZHOU  = 2069365345938698241
provider_sc = {}
for _, mu in member_users.iterrows():
    uid = int(mu["id"]) if pd.notna(mu.get("id")) else 0
    prov = str(mu.get("provider", "")).strip().lower() if pd.notna(mu.get("provider")) else ""
    if not uid: continue
    if uid in mu_sc or uid in user_sc: continue
    provider_sc[uid] = SC_CHANGZHOU if prov == "szd" else SC_WENZHOU

wal_uid, wal_bal = {}, {}
wal_real_uids = set()
uid_wid = {}  # user_id → wallet_id
for _, w in wallets.iterrows():
    wid = int(w["id"]) if pd.notna(w.get("id")) else 0
    uid = int(w["user_id"]) if pd.notna(w.get("user_id")) else 0
    if wid: wal_uid[wid] = uid
    if uid:
        wal_bal[uid] = int(w["balance"]) if pd.notna(w.get("balance")) else 0
        ut = int(w["user_type"]) if pd.notna(w.get("user_type")) else 0
        if ut == 1: wal_real_uids.add(uid)
        uid_wid[uid] = wid

# sc_id → SC wallet_id (通过 virtual_user_id 中转)
sc_wallet = {}
for _, s in stations.iterrows():
    sc_id = int(s["id"]) if pd.notna(s.get("id")) else 0
    vu = int(s["virtual_user_id"]) if pd.notna(s.get("virtual_user_id")) else 0
    if sc_id and vu and vu in uid_wid:
        sc_wallet[sc_id] = uid_wid[vu]

# 快速查找集
ro_set = set(); ro_info = {}
for _, ro in recycle_orders.iterrows():
    rid_raw = ro.get("id")
    try: rid = str(_to_int(rid_raw)) if pd.notna(rid_raw) else ""
    except: continue
    if rid:
        ro_set.add(rid)
        ro_info[rid] = {
            "uid": _to_int(ro["user_id"]),
            "oc": _to_int(ro["operation_center_id"]),
            "pay_type": int(ro.get("pay_type", 1)) if pd.notna(ro.get("pay_type")) and str(ro.get("pay_type")).replace('.','').lstrip('-').isdigit() else 1,
            "order_type": int(ro.get("order_type", 0)) if pd.notna(ro.get("order_type")) and str(ro.get("order_type")).replace('.','').lstrip('-').isdigit() else 0,
        }

wd_set = set(); wd_info = {}
for _, wd in withdraws.iterrows():
    did = str(int(wd["id"])) if pd.notna(wd.get("id")) else ""
    if did:
        wd_set.add(did)
        wd_info[did] = {
            "uid": int(wd["user_id"]) if pd.notna(wd.get("user_id")) else 0,
            "user_type": int(wd["user_type"]) if pd.notna(wd.get("user_type")) else 0,
            "type": int(wd.get("type", 1)) if pd.notna(wd.get("type")) else 1,
        }

# virtual_user_id → station name 反向映射（报告用）
vu_name = {}
for _, s in stations.iterrows():
    v = int(s["virtual_user_id"]) if pd.notna(s.get("virtual_user_id")) else 0
    if v: vu_name[v] = str(s.get("name", ""))

# ============================================================
# 回放 (正序)
# ============================================================
def _resolve_oc(wallet_user_id, ro_oc=0):
    """SC归属三级降级：回收单OC → member_user → user_sc → provider_sc"""
    if ro_oc and ro_oc in sc_ids:
        return ro_oc
    oc = mu_sc.get(wallet_user_id, 0)
    if oc: return oc
    oc = user_sc.get(wallet_user_id, 0)
    if oc: return oc
    oc = provider_sc.get(wallet_user_id, 0)
    if oc: return oc
    return 0

sc_total = defaultdict(int); sc_wechat = defaultdict(int); sc_alipay = defaultdict(int)
sc_balance = defaultdict(int); sc_pending = defaultdict(int); user_bal = defaultdict(int)
# 从 pay_fund 基线起步
for sc_id in sc_ids:
    sc_total[sc_id] = sc_baseline_total.get(sc_id, 0)
    sc_wechat[sc_id] = sc_baseline_wechat.get(sc_id, 0)
    sc_alipay[sc_id] = sc_baseline_alipay.get(sc_id, 0)
# SC 余额从钱包当前值起步
for sc_id in sc_ids:
    if sc_id in sc_wallet:
        wid = sc_wallet[sc_id]
        vu_id = wal_uid.get(wid, 0)
        sc_balance[sc_id] = wal_bal.get(vu_id, 0)

# DEBUG: 常州分拣中心基线链路
SC_CZ_DEBUG = 2071977701136384001
print(f"\n[DEBUG] 常州 sc_wallet={sc_wallet.get(SC_CZ_DEBUG, 'MISSING')}")
wid_debug = sc_wallet.get(SC_CZ_DEBUG, 0)
if wid_debug:
    vu_debug = wal_uid.get(wid_debug, 0)
    print(f"[DEBUG] 常州 wallet_id={wid_debug} → user_id={vu_debug} → wal_bal={wal_bal.get(vu_debug, 'MISSING')}")
    # 同时检查 wallets 原始数据
    uid_wid_inv = {v: k for k, v in uid_wid.items()}
    print(f"[DEBUG] uid_wid[{vu_debug}]={uid_wid.get(vu_debug, 'MISSING')}")
    print(f"[DEBUG] wal_uid[{wid_debug}]={wal_uid.get(wid_debug, 'MISSING')}")
else:
    print(f"[DEBUG] sc_wallet 中无常州, 检查 uid_wid: vu=2071977701514149889, wid={uid_wid.get(2071977701514149889, 'MISSING')}")

_no_sc_users = defaultdict(list)  # user_id → [时间列表]
fund_flows = []  # 基金变动流水记录
wallet_flows = []  # SC钱包余额流水记录

print("\n" + "=" * 60)
print("流水明细")
print("=" * 60)

for _, tx in trans.sort_values("create_time").iterrows():
    tx_title = str(tx.get("title", "")).strip()
    bid = tx.get("biz_id")
    biz = str(int(bid)) if pd.notna(bid) and str(bid).replace('.','').isdigit() else (str(bid) if pd.notna(bid) else "")
    wid = int(tx["wallet_id"]) if pd.notna(tx.get("wallet_id")) else 0
    uid = wal_uid.get(wid, 0)
    if uid not in wal_real_uids: continue  # 仅处理真实用户 (user_type=1)
    p = float(tx["price"]) if pd.notna(tx.get("price")) else 0
    amt = abs(int(p))
    if not amt: continue

    # ── 提现 ──
    if tx_title == "提现":
        # user_type=1 为用户提现；过滤网点人员
        if biz not in wd_set or wd_info[biz]["user_type"] != 1: continue
        wallet_user_id = wal_uid.get(wid, 0)
        if not wallet_user_id: continue
        if wallet_user_id in sys_uid_set: continue
        oc = _resolve_oc(wallet_user_id)
        if not oc:
            tx_time = tx.get("create_time")
            _no_sc_users[wallet_user_id].append(str(tx_time) if pd.notna(tx_time) else "未知")
            print(f"  [跳过-无SC归属] 提现 流水ID={tx.get('id')} 用户={wallet_user_id} 时间={tx_time}")
            continue
        wd = wd_info[biz]
        is_ali = wd["type"] in (1, 5, 6, 7)
        channel = "支付宝" if is_ali else "微信"
        # price<0 → 出金
        before_total = sc_total[oc]; before_wechat = sc_wechat[oc]; before_alipay = sc_alipay[oc]
        sc_pending[oc] -= amt; sc_total[oc] -= amt; user_bal[wallet_user_id] -= amt
        if is_ali: sc_alipay[oc] -= amt
        else: sc_wechat[oc] -= amt
        fund_flows.append({
            "sc_id": oc, "biz_id": biz, "flow_type": 50,
            "trade_channel": 2 if is_ali else 1, "trade_amount": -amt,
            "before_total": before_total, "after_total": sc_total[oc],
            "before_wechat": before_wechat, "after_wechat": sc_wechat[oc],
            "before_alipay": before_alipay, "after_alipay": sc_alipay[oc],
            "create_time": tx.get("create_time"),
            "update_time": tx.get("update_time"),
        })
        print(f"  [用户提现-{channel}] 流水ID={tx.get('id')} 提现单={biz} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")

    # ── 提现失败返还 ──
    elif tx_title == "提现失败返还":
        if biz not in wd_set or wd_info[biz]["user_type"] != 1: continue
        wallet_user_id = wal_uid.get(wid, 0)
        if not wallet_user_id: continue
        if wallet_user_id in sys_uid_set: continue
        oc = _resolve_oc(wallet_user_id)
        if not oc:
            tx_time = tx.get("create_time")
            _no_sc_users[wallet_user_id].append(str(tx_time) if pd.notna(tx_time) else "未知")
            print(f"  [跳过-无SC归属] 提现返还 流水ID={tx.get('id')} 用户={wallet_user_id} 时间={tx_time}")
            continue
        wd = wd_info[biz]
        is_ali = wd["type"] in (1, 5, 6, 7)
        channel = "支付宝" if is_ali else "微信"
        # price>0 → 入金
        before_total = sc_total[oc]; before_wechat = sc_wechat[oc]; before_alipay = sc_alipay[oc]
        sc_pending[oc] += amt; sc_total[oc] += amt; user_bal[wallet_user_id] += amt
        if is_ali: sc_alipay[oc] += amt
        else: sc_wechat[oc] += amt
        fund_flows.append({
            "sc_id": oc, "biz_id": biz, "flow_type": 10,
            "trade_channel": 2 if is_ali else 1, "trade_amount": amt,
            "before_total": before_total, "after_total": sc_total[oc],
            "before_wechat": before_wechat, "after_wechat": sc_wechat[oc],
            "before_alipay": before_alipay, "after_alipay": sc_alipay[oc],
            "create_time": tx.get("create_time"),
            "update_time": tx.get("update_time"),
        })
        print(f"  [提现返还-{channel}] 流水ID={tx.get('id')} 提现单={biz} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")

    # ── 回收结算 ──
    elif tx_title == "回收结算":
        if biz not in ro_set: continue
        ro = ro_info[biz]
        if ro["order_type"] != 0: continue
        wallet_user_id = uid
        ro_oc = ro["oc"] if ro["oc"] in sc_ids else 0
        oc = _resolve_oc(wallet_user_id, ro_oc)
        if not oc:
            tx_time = tx.get("create_time")
            _no_sc_users[wallet_user_id].append(str(tx_time) if pd.notna(tx_time) else "未知")
            print(f"  [跳过-无SC归属] 回收结算 流水ID={tx.get('id')} 用户={wallet_user_id} 时间={tx_time}")
            continue
        # price>0 → 到钱包
        sc_balance[oc] -= amt; sc_pending[oc] += amt; user_bal[wallet_user_id] += amt
        if oc in sc_wallet:
            wallet_flows.append({
                "sc_id": oc, "wallet_id": sc_wallet[oc], "biz_id": biz,
                "biz_type": int(tx.get("biz_type", 0)) if pd.notna(tx.get("biz_type")) else 0,
                "title": tx_title, "price": -amt, "balance": sc_balance[oc],
                "create_time": tx.get("create_time"),
                "update_time": tx.get("update_time"),
            })
        print(f"  [回收结算-到钱包] 流水ID={tx.get('id')} 订单={biz} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")

    # ── 转账 (老数据=回收结算到钱包) ──
    elif tx_title == "转账":
        wallet_user_id = uid
        oc = _resolve_oc(wallet_user_id)
        if not oc:
            tx_time = tx.get("create_time")
            _no_sc_users[wallet_user_id].append(str(tx_time) if pd.notna(tx_time) else "未知")
            print(f"  [跳过-无SC归属] 转账 流水ID={tx.get('id')} 用户={wallet_user_id} 时间={tx_time}")
            continue
        sc_balance[oc] -= amt; sc_pending[oc] += amt; user_bal[wallet_user_id] += amt
        if oc in sc_wallet:
            wallet_flows.append({
                "sc_id": oc, "wallet_id": sc_wallet[oc], "biz_id": biz,
                "biz_type": int(tx.get("biz_type", 0)) if pd.notna(tx.get("biz_type")) else 0,
                "title": tx_title, "price": -amt, "balance": sc_balance[oc],
                "create_time": tx.get("create_time"),
                "update_time": tx.get("update_time"),
            })
        print(f"  [转账-到钱包] 流水ID={tx.get('id')} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")

    # ── 其它 title (充值/清运结算/支付等) 跳过 ──
    else:
        continue

# ============================================================
# 输出
# ============================================================
print("=" * 60)
print("资金初始化 — 统计报告 (初始值)")
print("=" * 60)

sc_fund = {}

# 构建 分拣中心 → 用户集合 (合并 mu_sc + user_sc + provider_sc)
sc_users = defaultdict(set)
for uid, sc_id in mu_sc.items():
    sc_users[sc_id].add(uid)
for uid, sc_id in user_sc.items():
    sc_users[sc_id].add(uid)
for uid, sc_id in provider_sc.items():
    sc_users[sc_id].add(uid)

for sc_id in sorted(sc_ids):
    t, w2, a2 = sc_total[sc_id], sc_wechat[sc_id], sc_alipay[sc_id]
    b, p2 = sc_balance[sc_id], sc_pending[sc_id]
    sc_fund[sc_id] = {"total": t, "wechat": w2, "alipay": a2, "balance": b, "pending": p2}
    
    users_in_sc = sc_users[sc_id]
    user_sum = sum(user_bal.get(u, 0) for u in users_in_sc)
    wallet_sum = sum(wal_bal.get(u, 0) for u in users_in_sc)
    
    print(f"\n  分拣中心：{sc_name[sc_id]}")
    print(f"    总资金：{t}  微信资金：{w2}  支付宝资金：{a2}")
    print(f"    余额：{b}  待提现金额：{p2}")
    print(f"    所属用户数：{len(users_in_sc)}")
    print(f"    用户余额总和：{user_sum}  钱包余额总和：{wallet_sum}")
    print(f"    待提现校验（公式：待提现=用户余额总和）：{'✅' if p2 == user_sum else '❌ 待提现=' + str(p2) + ' 用户余额和=' + str(user_sum)}")

# ============================================================
# 校验：用户余额  vs  钱包余额
# ============================================================
print("\n" + "=" * 60)
print("校验：计算的用户余额 vs 实际钱包余额")
print("=" * 60)

balance_mismatch = 0
all_check_users = (set(user_bal.keys()) | set(wal_bal.keys())) & wal_real_uids

for uid in sorted(all_check_users):
    calc = user_bal.get(uid, 0)
    actual = wal_bal.get(uid, 0)
    if calc != actual:
        balance_mismatch += 1
        if balance_mismatch <= 20:
            sc_name_ref = sc_name.get(mu_sc.get(uid, 0), sc_name.get(user_sc.get(uid, 0), sc_name.get(provider_sc.get(uid, 0), vu_name.get(uid, "未知"))))
            print(f"  ❌ 用户={uid} {sc_name_ref}  计算余额={calc}  钱包余额={actual}  差额={calc - actual}")

if balance_mismatch == 0:
    print("  ✅ 所有用户余额完全一致")
else:
    print(f"\n  ⚠️ 共 {balance_mismatch} 个用户余额不一致")

# ============================================================
# 待手动核对的用户（member_user 和 recycle_order 都找不到 SC）
# ============================================================
if _no_sc_users:
    print("\n" + "=" * 60)
    print("待手动核对的用户（member_user 和 recycle_order 都无分拣中心归属）")
    print("=" * 60)
    for uid in sorted(_no_sc_users.keys()):
        times = _no_sc_users[uid]
        print(f"  user_id={uid}  流水时间: {', '.join(times)}")
    print(f"\n  共 {len(_no_sc_users)} 个用户需要手动核对分拣中心归属")

# ============================================================
# SQL
# ============================================================
print(f"\n生成 SQL → {OUTPUT_SQL}\n")

def esc(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return "NULL"
    if isinstance(v, (int, np.integer)): return str(int(v))
    if isinstance(v, (float, np.floating)): return str(int(v)) if not pd.isna(v) else "NULL"
    if isinstance(v, datetime): return f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'"
    return "'" + str(v).replace("\\","\\\\").replace("'","\\'") + "'"

def esc_dt(v):
    if pd.isna(v): return "NOW()"
    try: return f"'{pd.Timestamp(v).strftime('%Y-%m-%d %H:%M:%S')}'"
    except: return "NOW()"

sql = []; L = lambda line="": sql.append(line)
L("-- ============================================")
L(f"-- 资金初始化 SQL ({datetime.now():%Y-%m-%d %H:%M})")
L("-- ============================================"); L(); L("BEGIN;"); L()

stat_fund_flow = stat_wallet_flow = 0

for cid in sorted(comp_ids):
    c_sc = {s: st for s, st in sc_fund.items() if sc_company.get(s) == cid}
    if not c_sc: continue
    cname = f"公司{cid}"
    L(f"-- === 公司: {cname} (orgId={cid}) ===\n")

    # pay_fund_flow (提现/提现返还)
    sc_flows = [f for f in fund_flows if f["sc_id"] in c_sc]
    sc_flows.sort(key=lambda x: x.get("create_time") if pd.notna(x.get("create_time")) else pd.Timestamp.min)
    for fl in sc_flows:
        pfid = sc_pay_fund.get(fl["sc_id"])
        if not pfid: continue
        L(f"-- {sc_name.get(fl['sc_id'], '')} flow_type={fl['flow_type']} channel={fl['trade_channel']}")
        L(f"INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, "
          f"trade_amount, before_balance, after_balance, "
          f"wechat_before_balance, wechat_after_balance, "
          f"alipay_before_balance, alipay_after_balance, "
          f"creator, updater, create_time, update_time, deleted, tenant_id) VALUES ("
          f"{pfid}, {esc(fl['biz_id'])}, {fl['sc_id']}, {fl['flow_type']}, {fl['trade_channel']}, "
          f"{fl['trade_amount']}, {fl['before_total']}, {fl['after_total']}, "
          f"{fl['before_wechat']}, {fl['after_wechat']}, "
          f"{fl['before_alipay']}, {fl['after_alipay']}, "
          f"0, 0, {esc_dt(fl['create_time'])}, {esc_dt(fl['update_time'])}, 0, {TENANT_ID});")
        stat_fund_flow += 1

    # pay_wallet_transaction (回收结算/转账 — SC钱包余额流水)
    wl = [w for w in wallet_flows if w["sc_id"] in c_sc]
    wl.sort(key=lambda x: x.get("create_time") if pd.notna(x.get("create_time")) else pd.Timestamp.min)
    for w in wl:
        L(f"-- {sc_name.get(w['sc_id'], '')} {w['title']} wallet_tx")
        L(f"INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, "
          f"creator, updater, create_time, update_time, deleted, tenant_id) VALUES ("
          f"{w['wallet_id']}, {w['biz_type']}, {esc(w['biz_id'])}, {esc(w['title'])}, {w['price']}, {w['balance']}, "
          f"0, 0, {esc_dt(w['create_time'])}, {esc_dt(w['update_time'])}, 0, {TENANT_ID});")
        stat_wallet_flow += 1

    # pay_fund UPDATE (平帐：基线 + 消费 = 最终值)
    for sc_id in c_sc:
        if sc_id not in sc_pay_fund: continue
        st = sc_fund[sc_id]
        L(f"-- {sc_name[sc_id]} pay_fund UPDATE")
        L(f"UPDATE pay_fund SET total_fund={st['total']}, wechat_fund={st['wechat']}, "
          f"alipay_fund={st['alipay']}, updater=0, update_time=NOW() "
          f"WHERE fund_type=20 AND org_id={sc_id};")

L(); L("COMMIT;"); L()
L(f"-- fund_flow={stat_fund_flow}  wallet_flow={stat_wallet_flow}")

with open(OUTPUT_SQL, "w", encoding="utf-8") as f: f.write("\n".join(sql))
print(f"✅ fund_flow: {stat_fund_flow}  wallet_flow: {stat_wallet_flow}")

# 按分拣中心拆分输出
output_dir = os.path.dirname(OUTPUT_SQL)
sc_count = 0
for sc_id in sorted(sc_ids):
    sc_nm = sc_name[sc_id]
    if SC_FILTER and sc_nm not in SC_FILTER:
        continue
    sc_sql = []; sL = lambda line="": sc_sql.append(line)
    sL("-- ============================================")
    sL(f"-- 资金初始化 SQL - {sc_nm} ({datetime.now():%Y-%m-%d %H:%M})")
    sL("-- ============================================"); sL(); sL("BEGIN;"); sL()

    sc_flows = [f for f in fund_flows if f["sc_id"] == sc_id]
    sc_flows.sort(key=lambda x: x.get("create_time") if pd.notna(x.get("create_time")) else pd.Timestamp.min)
    for fl in sc_flows:
        pfid = sc_pay_fund.get(sc_id)
        if not pfid: continue
        sL(f"-- flow_type={fl['flow_type']} channel={fl['trade_channel']}")
        sL(f"INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, "
          f"trade_amount, before_balance, after_balance, "
          f"wechat_before_balance, wechat_after_balance, "
          f"alipay_before_balance, alipay_after_balance, "
          f"creator, updater, create_time, update_time, deleted, tenant_id) VALUES ("
          f"{pfid}, {esc(fl['biz_id'])}, {sc_id}, {fl['flow_type']}, {fl['trade_channel']}, "
          f"{fl['trade_amount']}, {fl['before_total']}, {fl['after_total']}, "
          f"{fl['before_wechat']}, {fl['after_wechat']}, "
          f"{fl['before_alipay']}, {fl['after_alipay']}, "
          f"0, 0, {esc_dt(fl['create_time'])}, {esc_dt(fl['update_time'])}, 0, {TENANT_ID});")

    wl = [w for w in wallet_flows if w["sc_id"] == sc_id]
    wl.sort(key=lambda x: x.get("create_time") if pd.notna(x.get("create_time")) else pd.Timestamp.min)
    for w in wl:
        sL(f"-- {w['title']} wallet_tx")
        sL(f"INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, "
          f"creator, updater, create_time, update_time, deleted, tenant_id) VALUES ("
          f"{w['wallet_id']}, {w['biz_type']}, {esc(w['biz_id'])}, {esc(w['title'])}, {w['price']}, {w['balance']}, "
          f"0, 0, {esc_dt(w['create_time'])}, {esc_dt(w['update_time'])}, 0, {TENANT_ID});")

    st = sc_fund[sc_id]
    if sc_id in sc_pay_fund:
        sL(f"-- pay_fund UPDATE")
        sL(f"UPDATE pay_fund SET total_fund={st['total']}, wechat_fund={st['wechat']}, "
          f"alipay_fund={st['alipay']}, updater=0, update_time=NOW() "
          f"WHERE fund_type=20 AND org_id={sc_id};")

    sL(); sL("COMMIT;")
    fname = f"init_fund_{sc_nm.replace('/', '_')}_{datetime.now():%Y%m%d_%H%M}.sql"
    fpath = os.path.join(output_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f: f.write("\n".join(sc_sql))
    sc_count += 1
    print(f"  📄 {fname}")

if sc_count:
    print(f"✅ 按SC拆分: {sc_count} 个文件")

