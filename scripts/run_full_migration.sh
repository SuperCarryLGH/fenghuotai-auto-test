#!/usr/bin/env bash
# 全量数据迁移模拟编排器（本地库 → dev 影子表）
# 用法: nohup bash scripts/run_full_migration.sh > logs/master.log 2>&1 &
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

# 源=同事本地库（模拟）；target 比对仍读 online.xlsx（脚本内 DEP_SOURCE=xlsx）
export OLD_DB_HOST=192.168.0.231
export OLD_DB_PORT=3306
export OLD_DB_USER=root
export OLD_DB_PASSWORD=123456
export OLD_DB_DATABASE=yihuishou

mark() { echo "=== $(date '+%F %T') $1 ==="; }

run_phase() {
    local name="$1" script="$2" args="${3:-}"
    mark "START $name"
    ( cd "$ROOT/scripts" && "$PY" "$script" $args ) >> "$LOG_DIR/$name.log" 2>&1
    local code=$?
    mark "END $name exit=$code"
    if [ "$code" -ne 0 ]; then
        mark "ABORT 全量流程在 $name 失败(exit=$code)，后续阶段已终止"
        tail -n 30 "$LOG_DIR/$name.log"
        exit "$code"
    fi
    echo "--- $name 日志尾部 ---"
    tail -n 3 "$LOG_DIR/$name.log"
}

mark "FULL MIGRATION START"
run_phase 01_four_table migrate_old_db_to_shadow.py
run_phase 02_sync_action mark_sync_action.py
run_phase 03_dist migrate_dist.py
# 3b. 佣金账户（纯 dev 派生，依赖 dist_promoter）
run_phase 03b_commission migrate_dist_commission_account.py
run_phase 04_order_online migrate_order.py
run_phase 05_package migrate_package_item.py
# 6. 线下订单（面对面）——默认关，MIGRATE_OFFLINE=1 才执行
if [ "${MIGRATE_OFFLINE:-0}" = "1" ]; then
    run_phase 06_order_offline migrate_order.py "--offline"
else
    mark "SKIP 06_order_offline（MIGRATE_OFFLINE 未开启，面对面订单不处理）"
fi
run_phase 07_backfill backfill_operation_center_id.py
run_phase 08_pollution gen_pollution_list.py
mark "FULL MIGRATION DONE (all phases exit=0)"
