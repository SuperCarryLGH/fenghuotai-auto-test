#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分销迁移独立脚本（方案 B）：promotion_promoter → shadow_dist_promoter，
以及 sys_user.promoter_id → shadow_dist_promoter_user_relation。

- 顺序：先 dist_promoter（建立 老promoter_id→新dist_promoter.id 映射）→ 再 relation
- 复用：by_account（account_id→新member_user.id）、gen_id、insert_batch、断点续传
- 未命中映射（account 不在新用户 / promoter 不在新推广员）→ 跳过并在报告列出
- 影子表结构与 dev 一致（金额分×100、重量 decimal(10,2)）

用法：
    python scripts/migrate_dist.py --init      # 只建影子表
    python scripts/migrate_dist.py --reset     # 清空影子表+状态
    python scripts/migrate_dist.py --limit N   # 试运行前N条推广员
    python scripts/migrate_dist.py             # 全量（断点续跑）
"""
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql.cursors import DictCursor  # noqa: E402

from migrate_old_db_to_shadow import (  # noqa: E402
    db, DEV_DB, OLD_DB, BATCH, gen_id, insert_batch, rebuild_by_account,
    load_target_users, to_int, to_fen,
)

STATE_FILE = PROJECT_ROOT / "scripts" / ".migrate_dist_state.json"
SHADOW_TABLES = {
    "dist_promoter": "shadow_dist_promoter",
    "dist_promoter_user_relation": "shadow_dist_promoter_user_relation",
}


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def create_shadow_tables(conn):
    cur = conn.cursor()
    for src, shadow in SHADOW_TABLES.items():
        cur.execute("SHOW TABLES LIKE %s", (shadow,))
        if cur.fetchone():
            print(f"  影子表已存在: {shadow}")
            continue
        cur.execute(f"CREATE TABLE `{shadow}` LIKE `{src}`")
        print(f"  ✅ 创建影子表 {shadow} (like {src})")
    conn.commit()


def load_user_map(old_conn, dev_conn):
    """account_id(UUID) -> 新 member_user.id（含已存在用户）"""
    ba = rebuild_by_account(old_conn, dev_conn, load_target_users())
    return {acc: info["uid"] for acc, info in ba.items()}


def load_promoter_source_map(old_conn):
    """旧 sys_user 的实名/昵称/头像/创建时间/上下级（按 account_id）"""
    cur = old_conn.cursor()
    cur.execute(
        "SELECT account_id, real_auth_name, real_auth_id, nick_name, avatar, "
        "created_at, promoter_id, promoter_agent_id FROM sys_user "
        "WHERE role_id=5 AND account_id IS NOT NULL AND account_id<>''")
    out = {}
    for r in cur.fetchall():
        out[str(r["account_id"])] = r
    return out


def migrate_dist_promoter(old_conn, dev_conn, user_map, src_map, state, limit=0):
    key = "dist_promoter"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  dist_promoter 已迁移完成，跳过")
        return {}
    cur = old_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    last = st["last_id"]
    rows_done = st["rows"]
    promoter_id_map = {}      # 旧 promoter_id(UUID) -> 新 dist_promoter.id
    promoter_accounts = {}    # 旧 promoter_id -> account_id（用于 parent 回填）
    skipped = 0
    batch_no = 0
    while True:
        cur.execute("SELECT * FROM promotion_promoter WHERE id > %s ORDER BY id LIMIT %s", (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = []
        for r in rows:
            uid = user_map.get(str(r["account_id"] or ""))
            if not uid:
                skipped += 1
                continue
            s = src_map.get(str(r["account_id"] or ""), {})
            real_name = s.get("real_auth_name") or ""
            nid = gen_id()
            promoter_id_map[str(r["promoter_id"])] = nid
            promoter_accounts[str(r["promoter_id"])] = str(r["account_id"] or "")
            to_insert.append({
                "id": nid,
                "user_id": uid,
                "apply_id": 0,
                "real_name": real_name,
                "id_card": s.get("real_auth_id") or "",
                "id_card_front": "",
                "id_card_back": "",
                "auth_status": 30 if real_name else 10,
                "operate_agreement_url": "",
                "operate_agreement_status": 0,
                "qrcode_wechat": None,
                "qrcode_alipay": None,
                "qrcode_douyin": None,
                "qrcode_kuaishou": None,
                "qrcode_normal": None,
                "parent_promoter_id": None,
                "grand_promoter_id": None,
                "promoter_level": 1,
                "promoter_star": 1,
                "promoter_type": 10,
                "open_source": 10,
                "open_time": r.get("approve_time"),
                "close_time": None,
                "status": 1,
                "team_id": 0,
                "first_promote_user_num": 0,
                "second_promote_user_num": 0,
                "first_order_count": 0,
                "second_order_count": 0,
                "first_order_amount": 0,
                "second_order_amount": 0,
                "first_order_weight": 0,
                "second_order_weight": 0,
                "creator": "migrate",
                "create_time": r.get("created_at") or now,
                "updater": "migrate",
                "update_time": now,
                "deleted": b"\x00",
                "tenant_id": 1,
                "real_name_auth_status": 1 if real_name else 0,
                "auth_remark": None,
                "auth_submit_time": None,
                "auth_check_time": None,
                "first_order_complete_count": 0,
                "second_order_complete_count": 0,
            })
        insert_batch(dev_conn, SHADOW_TABLES[key], to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_state({**state, key: st})
        batch_no += 1
        if batch_no % 20 == 0:
            print(f"  [dist_promoter] 第{batch_no}批: 累计{rows_done}")
        if limit and rows_done >= limit:
            break
    # 回填 parent/grand_promoter_id（推广人自己的上级，用已收集的 promoter_accounts）
    parent_updates = []
    for pid, acc in promoter_accounts.items():
        s = src_map.get(acc, {})
        nid = promoter_id_map.get(pid)
        if not nid:
            continue
        pp = promoter_id_map.get(str(s.get("promoter_id") or ""))
        gp = promoter_id_map.get(str(s.get("promoter_agent_id") or ""))
        if pp is not None or gp is not None:
            parent_updates.append((pp, gp, nid))
        if len(parent_updates) >= BATCH:
            _apply_parent(dev_conn, parent_updates)
            parent_updates = []
    if parent_updates:
        _apply_parent(dev_conn, parent_updates)
    if not limit:
        st["done"] = True
    save_state({**state, key: st})
    print(f"  ✅ dist_promoter 迁移完成，共 {rows_done} 行（跳过未映射 {skipped}）")
    return promoter_id_map


def _apply_parent(dev_conn, updates):
    """回填 parent/grand：临时表 + 批量 INSERT + 一次 JOIN UPDATE
    （原逐行 executemany UPDATE 到远程 RDS 极慢且易挂，改为批量）"""
    cur = dev_conn.cursor()
    cur.execute("DROP TEMPORARY TABLE IF EXISTS _tmp_parent")
    cur.execute(
        "CREATE TEMPORARY TABLE _tmp_parent "
        "(id bigint PRIMARY KEY, pp bigint NULL, gp bigint NULL)")
    cur.executemany(
        "INSERT INTO _tmp_parent (id, pp, gp) VALUES (%s, %s, %s)",
        [(n, p, g) for p, g, n in updates])
    cur.execute(
        "UPDATE shadow_dist_promoter d JOIN _tmp_parent t ON t.id=d.id "
        "SET d.parent_promoter_id=t.pp, d.grand_promoter_id=t.gp")
    dev_conn.commit()
    cur.execute("DROP TEMPORARY TABLE IF EXISTS _tmp_parent")


def migrate_dist_relation(old_conn, dev_conn, user_map, promoter_id_map, src_map, state, limit=0):
    key = "dist_promoter_user_relation"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  dist_promoter_user_relation 已迁移完成，跳过")
        return
    cur = old_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    last = st["last_id"]
    rows_done = st["rows"]
    skipped = 0
    batch_no = 0
    while True:
        cur.execute(
            "SELECT u.id, u.account_id, u.promoter_id, u.nick_name, u.avatar, u.created_at, "
            "p.account_id AS promoter_account "
            "FROM sys_user u JOIN promotion_promoter p ON p.promoter_id = u.promoter_id "
            "WHERE u.role_id=5 AND u.promoter_id<>'' AND u.id > %s ORDER BY u.id LIMIT %s",
            (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = []
        for r in rows:
            uid = user_map.get(str(r["account_id"] or ""))
            pid = promoter_id_map.get(str(r["promoter_id"] or ""))
            p_uid = user_map.get(str(r["promoter_account"] or ""))
            if not uid or not pid or not p_uid:
                skipped += 1
                continue
            ps = src_map.get(str(r["promoter_account"] or ""), {})
            parent_pid = promoter_id_map.get(str(ps.get("promoter_id") or ""))   # 推广人的上一级
            to_insert.append({
                "id": gen_id(),
                "parent_promoter_id": parent_pid,
                "promoter_id": pid,
                "promotor_user_id": p_uid,
                "user_id": uid,
                "user_name": r.get("nick_name"),
                "avatar": r.get("avatar"),
                "promoter_type": 1,
                "team_id": None,
                "bind_source": 10,
                "bind_time": r.get("created_at") or now,
                "status": 1,
                "remark": "用户注册时绑定推广关系",
                "creator": "migrate",
                "create_time": now,
                "updater": "migrate",
                "update_time": now,
                "deleted": b"\x00",
                "tenant_id": 1,
            })
        insert_batch(dev_conn, SHADOW_TABLES[key], to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_state({**state, key: st})
        batch_no += 1
        if batch_no % 20 == 0:
            print(f"  [relation] 第{batch_no}批: 累计{rows_done}")
        if limit and rows_done >= limit:
            break
    st["done"] = True
    save_state({**state, key: st})
    print(f"  ✅ dist_promoter_user_relation 迁移完成，共 {rows_done} 行（跳过 {skipped}）")


def main():
    args = sys.argv[1:]
    old_conn = db(OLD_DB)
    dev_conn = db(DEV_DB)
    state = load_state()

    if "--init" in args:
        create_shadow_tables(dev_conn)
        print("分销影子表创建完成")
        return
    if "--reset" in args:
        for t in SHADOW_TABLES.values():
            dev_conn.cursor().execute(f"DROP TABLE IF EXISTS `{t}`")
        dev_conn.commit()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("已清空分销影子表与状态")
        return

    create_shadow_tables(dev_conn)
    limit = 0
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
        print(f"试运行模式：前 {limit} 条推广员")

    print("加载 account_id -> 新 member_user.id 映射...")
    user_map = load_user_map(old_conn, dev_conn)
    print(f"  user_map: {len(user_map)}")
    print("加载旧 sys_user 实名/昵称/上下级...")
    src_map = load_promoter_source_map(old_conn)
    print(f"  src_map: {len(src_map)}")

    promoter_id_map = migrate_dist_promoter(old_conn, dev_conn, user_map, src_map, state, limit)
    migrate_dist_relation(old_conn, dev_conn, user_map, promoter_id_map, src_map, state, limit)
    print("\n分销迁移完成。可用 --limit 试跑 / 重新全量（断点续传）。")


if __name__ == "__main__":
    main()
