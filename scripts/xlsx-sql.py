#通用xlsx转sql方法，SRC：地址，sheet：分页名称，cols：参数字段填写（仅支持insert的sql的生成
import pandas as pd
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")
SRC = Path("/Users/rs/Documents/mock.xlsx")
OUT = SRC.parent / "mock_es_vehicle_task_record.sql"
SHEETS = ["08-04", "08-07"]
COLS = ["id", "organization_info_id", "es_vehicle_id", "vehicle_plate_number", "record_date",
        "total_work_distance", "total_travel_distance", "actual_work_distance",
        "work_completion_rate", "actual_work_duration", "anomaly_event_count",
        "departure_time", "arrival_time", "project_id", "add_time", "update_time", "deleted"]
def fmt_datetime(v):
    if pd.isna(v):
        return "NULL"
    return "'" + pd.Timestamp(v).strftime("%Y-%m-%d %H:%M:%S") + "'"
def fmt_date(v):
    return "'" + pd.Timestamp(v).strftime("%Y-%m-%d") + "'"
def fmt_num(v, nd=2):
    return f"{float(v):.{nd}f}"
def fmt_int(v):
    return str(int(v))
def value_sql(col, v):
    if pd.isna(v):
        return "NULL"
    if col in ("id", "organization_info_id", "es_vehicle_id", "vehicle_plate_number"):
        return f"'{str(v)}'"
    if col == "record_date":
        return fmt_date(v)
    if col in ("departure_time", "arrival_time", "add_time", "update_time"):
        return fmt_datetime(v)
    if col =="total_work_distance":
        return fmt_num(v/1000, 2)
    if col in ("total_travel_distance", "actual_work_distance",
               "work_completion_rate"):
        return fmt_num(v, 2)
    if col in ("actual_work_duration", "anomaly_event_count", "deleted"):
        return fmt_int(v)
    if col == "project_id":
        return "NULL"
    return f"'{str(v)}'"
lines = []
total = 0
for sh in SHEETS:
    df = pd.read_excel(SRC, sheet_name=sh,
                       dtype={"id": "object", "organization_info_id": "object",
                              "es_vehicle_id": "object"})
    for _, r in df.iterrows():
        vals = ", ".join(value_sql(c, r[c]) for c in COLS)
        lines.append(
            f"INSERT INTO `stdls`.`es_vehicle_task_record` "
            f"(`id`, `organization_info_id`, `es_vehicle_id`, `vehicle_plate_number`, `record_date`, "
            f"`total_work_distance`, `total_travel_distance`, `actual_work_distance`, `work_completion_rate`, "
            f"`actual_work_duration`, `anomaly_event_count`, `departure_time`, `arrival_time`, `project_id`, "
            f"`add_time`, `update_time`, `deleted`) "
            f"VALUES ({vals});"
        )
        total += 1

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"已生成 {OUT}: {total} 条 INSERT")
