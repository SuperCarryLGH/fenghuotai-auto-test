"""
资金初始化 v7 — 统计报告 + SQL 生成
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

DATA_SRC = "/Users/rs/Documents"
OUTPUT_SQL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Date", "init_fund.sql")
TENANT_ID = 1

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
system_users  = pd.read_excel(f"{DATA_SRC}/system_users.xlsx", dtype={"id": str}) if os.path.exists(f"{DATA_SRC}/system_users.xlsx") else None
member_users = pd.read_excel(f"{DATA_SRC}/member_user.xlsx", dtype={"id": str, "operation_center_id": str})

# system_users ID 集合 — 用于排除网点人员
sys_uid_set = set(int(x) for x in system_users["id"].dropna() if pd.notna(x)) if system_users is not None else set()

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

# 公司映射 (从 station.company_id + sc_fund 反推)
comp_set = {}
for sc_id, comp_id in sc_company.items():
    if comp_id not in comp_set:
        comp_set[comp_id] = {"id": comp_id, "name": f"公司{comp_id}", "code": "", "purpose": 2}

user_sc = {}
for _, ro in recycle_orders.iterrows():
    try:
        uid = _to_int(ro["user_id"])
        oc = _to_int(ro["operation_center_id"])
    except: continue
    if uid and oc in sc_ids: user_sc[uid] = oc

wal_uid, wal_bal = {}, {}
for _, w in wallets.iterrows():
    wid = int(w["id"]) if pd.notna(w.get("id")) else 0
    uid = int(w["user_id"]) if pd.notna(w.get("user_id")) else 0
    if wid: wal_uid[wid] = uid
    if uid: wal_bal[uid] = int(w["balance"]) if pd.notna(w.get("balance")) else 0

wd_channel = {}
for _, wd in withdraws.iterrows():
    did = str(int(wd["id"])) if pd.notna(wd.get("id")) else ""
    wtype = int(wd.get("type", 1)) if pd.notna(wd.get("type")) else 1
    wd_channel[did] = wtype

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

sc_vuids = set()
for _, s in sc_df.iterrows():
    v = int(s["virtual_user_id"]) if pd.notna(s.get("virtual_user_id")) else 0
    if v: sc_vuids.add(v)

# ============================================================
# 回放 (正序)
# ============================================================
sc_total = defaultdict(int); sc_wechat = defaultdict(int); sc_alipay = defaultdict(int)
sc_balance = defaultdict(int); sc_pending = defaultdict(int); user_bal = defaultdict(int)
_no_sc_users = defaultdict(list)  # user_id → [时间列表]

print("\n" + "=" * 60)
print("流水明细")
print("=" * 60)

for _, tx in trans.sort_values("create_time").iterrows():
    bid = tx.get("biz_id")
    biz = str(int(bid)) if pd.notna(bid) and str(bid).replace('.','').isdigit() else (str(bid) if pd.notna(bid) else "")
    wid = int(tx["wallet_id"]) if pd.notna(tx.get("wallet_id")) else 0
    uid = wal_uid.get(wid, 0)
    p = float(tx["price"]) if pd.notna(tx.get("price")) else 0
    amt = abs(int(p))
    if not amt: continue

    # ── 上门回收结算 (order_type=0) ──
    if biz in ro_set and ro_info[biz]["order_type"] == 0:
        if uid in sc_vuids:  # SC 钱包镜像记录，跳过
            print(f"  [跳过-SC镜像] 流水ID={tx.get('id')} 订单号={biz} 金额={amt}分")
            continue
        ro = ro_info[biz]
        oc = ro["oc"]
        if oc not in sc_ids:
            print(f"  [跳过-OC不存在] 流水ID={tx.get('id')} biz_id={biz} OC原始值={oc}")
            continue
        ba = int(tx["balance"]) if pd.notna(tx.get("balance")) else 0
        if ba - int(p) < ba and p > 0:
            # 用户余额增加 → 到钱包
            sc_balance[oc] -= amt; sc_pending[oc] += amt; user_bal[uid] += amt
            print(f"  [回收结算-到钱包] 流水ID={tx.get('id')} 订单={biz} 用户={uid} 分拣中心={oc} 金额={amt}分")
        else:
            # 到微信/支付宝
            is_ali = ro["pay_type"] == 2
            channel = "支付宝" if is_ali else "微信"
            sc_total[oc] -= amt; sc_balance[oc] -= amt
            if is_ali: sc_alipay[oc] -= amt
            else: sc_wechat[oc] -= amt
            print(f"  [回收结算-到{channel}] 流水ID={tx.get('id')} 订单={biz} 用户={uid} 分拣中心={oc} 金额={amt}分")

    # ── 提现/返还 (biz_id 在 pay_withdraw, user_type=1) ──
    # 归属逻辑: wallet_id → pay_wallet.user_id → system_user过滤 → member_user.operation_center_id
    elif biz in wd_set and wd_info[biz]["user_type"] == 1:
        # 1. 通过 wallet_id → pay_wallet 拿到 user_id
        wallet_user_id = wal_uid.get(wid, 0)
        if not wallet_user_id:
            print(f"  [跳过-无wallet关联] 流水ID={tx.get('id')} biz_id={biz}")
            continue
        # 2. 排除网点人员（在 system_user 表中的跳过）
        if wallet_user_id in sys_uid_set:
            print(f"  [跳过-网点人员] 流水ID={tx.get('id')} 用户={wallet_user_id}")
            continue
        # 3. user_id → member_user → operation_center_id
        oc = mu_sc.get(wallet_user_id, 0)
        # 如果 member_user 里没有，降级到 recycle_order 查
        if not oc:
            oc = user_sc.get(wallet_user_id, 0)
        if not oc:
            tx_time = tx.get("create_time")
            _no_sc_users[wallet_user_id].append(str(tx_time) if pd.notna(tx_time) else "未知")
            print(f"  [跳过-无SC归属] 流水ID={tx.get('id')} 用户={wallet_user_id} 时间={tx_time}")
            continue
        wd = wd_info[biz]
        is_ali = wd["type"] in (1, 5, 6, 7)  # type: 1/5/6/7=支付宝, 2/4=微信
        channel = "支付宝" if is_ali else "微信"
        if p < 0:
            sc_pending[oc] -= amt; sc_total[oc] -= amt; user_bal[wallet_user_id] -= amt
            if is_ali: sc_alipay[oc] -= amt
            else: sc_wechat[oc] -= amt
            print(f"  [用户提现-{channel}] 流水ID={tx.get('id')} 提现单={biz} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")
        elif p > 0:
            sc_pending[oc] += amt; sc_total[oc] += amt; user_bal[wallet_user_id] += amt
            if is_ali: sc_alipay[oc] += amt
            else: sc_wechat[oc] += amt
            print(f"  [提现返还-{channel}] 流水ID={tx.get('id')} 提现单={biz} 用户={wallet_user_id} 分拣中心={oc} 金额={amt}分")

# ============================================================
# 输出
# ============================================================
print("=" * 60)
print("资金初始化 — 统计报告 (初始值)")
print("=" * 60)

sc_fund = {}

# 构建 分拣中心 → 用户集合 (合并 mu_sc + user_sc)
sc_users = defaultdict(set)
for uid, sc_id in mu_sc.items():
    sc_users[sc_id].add(uid)
for uid, sc_id in user_sc.items():
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
all_check_users = set(user_bal.keys()) | set(wal_bal.keys())

for uid in sorted(all_check_users):
    calc = user_bal.get(uid, 0)
    actual = wal_bal.get(uid, 0)
    if calc != actual:
        balance_mismatch += 1
        if balance_mismatch <= 20:
            sc_name_ref = sc_name.get(mu_sc.get(uid, 0), sc_name.get(user_sc.get(uid, 0), "未知"))
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

stat_fund = stat_sc = stat_flow = 0

for cid, comp in comp_set.items():
    cid = int(comp["id"]); cname = comp["name"]
    ccode = comp.get("code", ""); purp = comp.get("purpose", 2)
    c_sc = {s: st for s, st in sc_fund.items() if sc_company.get(s) == cid and len({u for u, sc in user_sc.items() if sc == s}) > 0}
    if not c_sc: continue

    comp_bal = sum(st["pending"] for st in c_sc.values())
    L(f"-- === 公司: {cname} (orgId={cid}) ===\n")
    L(f"INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, "
      f"allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (")
    L(f"  10, {cid}, {esc(ccode)}, {comp_bal}, {comp_bal}, 0, 0, {comp_bal}, {esc(cname)}, {esc(cname)}, {purp}, {TENANT_ID}, 'init_script', NOW(), NOW());\n")
    stat_fund += 1

    for sc_id, st in c_sc.items():
        L(f"INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, "
          f"allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (")
        L(f"  10, {sc_id}, {esc(ccode)}, {st['total']}, {st['wechat']}, {st['alipay']}, NULL, NULL, "
          f"{esc(cname)}, {esc(sc_name.get(sc_id, ''))}, {purp}, {TENANT_ID}, 'init_script', NOW(), NOW());\n")
        stat_sc += 1

    for _, tx in trans.sort_values("create_time").iterrows():
        wid = int(tx["wallet_id"]) if pd.notna(tx.get("wallet_id")) else 0
        uid = wal_uid.get(wid, 0); sc_id = user_sc.get(uid, 0)
        if sc_id not in c_sc: continue
        bt = int(tx.get("biz_type", 0)) if pd.notna(tx.get("biz_type")) else 0
        if bt not in (11, 8, 9): continue
        p = float(tx["price"]) if pd.notna(tx.get("price")) else 0
        bal = int(tx["balance"]) if pd.notna(tx.get("balance")) else 0
        ft = {11: 40, 8: 50, 9: 50}.get(bt, 0)
        L(f"-- {sc_name.get(sc_id)} bt={bt}")
        L(f"INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, "
          f"trade_amount, before_balance, after_balance, tenant_id, create_time) "
          f"SELECT id, {esc(tx.get('no'))}, {sc_id}, {ft}, 0, {abs(int(p))}, {bal - int(p)}, {bal}, "
          f"{TENANT_ID}, {esc_dt(tx.get('create_time'))} FROM pay_fund WHERE fund_type=10 AND org_id={sc_id} LIMIT 1;")
        stat_flow += 1

L(); L("COMMIT;"); L()
L(f"-- 公司={stat_fund} 分拣中心={stat_sc} 流水={stat_flow}")

with open(OUTPUT_SQL, "w", encoding="utf-8") as f: f.write("\n".join(sql))
print(f"✅ 公司: {stat_fund}  分拣中心: {stat_sc}  流水: {stat_flow}")
