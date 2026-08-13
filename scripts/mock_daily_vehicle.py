#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按"每天作业路线基本一样"的假设，用参照天(08-02/03/05/06/08)每辆车的中位数，
为 08-04 / 08-07 生成全量 mock 车辆工作记录，输出 mock.xlsx。

约束：
  - work_completion_rate = actual_work_distance / total_travel_distance
  - actual_work_duration 秒 = arrival_time - departure_time
  - es_vehicle_id 与车牌一一对应（日期格式单元格解码回 int）
  - 每行 update_time 有值
"""
import datetime
import random
import time
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

SRC = "/Users/rs/Documents/4号、七号.xlsx"
OUT = "/Users/rs/Documents/mock.xlsx"
REF_DAYS = ["08-02", "08-03", "08-05", "08-06", "08-08"]
MOCK_DAYS = ["2026-08-04", "2026-08-07"]
TARGET_ROWS = 87

# ---------- snowflake id（与现有 id 同构，19 位） ----------
_EPOCH = 1288834974657
_WORKER = 7
_SEQ = 0
_LAST_MS = 0
_USED = set()


def gen_id():
    global _SEQ, _LAST_MS
    for _ in range(100):
        now = int(time.time() * 1000)
        if now != _LAST_MS:
            _SEQ = 0
            _LAST_MS = now
        else:
            _SEQ += 1
        if _SEQ >= 4096:
            time.sleep(0.001)
            continue
        nid = ((now - _EPOCH) << 22) | (_WORKER << 12) | _SEQ
        if nid not in _USED:
            _USED.add(nid)
            return nid
    raise RuntimeError("id 生成碰撞")


# ---------- 读取参照天（id 类列用 object 读，避免 float64 丢精度） ----------
ref = {d: pd.read_excel(SRC, sheet_name=d,
                        dtype={"es_vehicle_id": "object", "organization_info_id": "object"})
       for d in REF_DAYS}


def decode_es_vehicle_id(v):
    """把 es_vehicle_id 归一为 int；日期格式单元格(如 1900-02-25)解码回 Excel 序列值(56)"""
    if pd.isna(v):
        return None
    if isinstance(v, datetime.datetime):
        return v.toordinal() - 693594 + (1 if v > datetime.datetime(1900, 3, 1) else 0)
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def median_of(plate, col):
    vals = []
    for d, df in ref.items():
        r = df[df["vehicle_plate_number"] == plate]
        if len(r):
            v = pd.to_numeric(r.iloc[0][col], errors="coerce")
            if pd.notna(v):
                vals.append(float(v))
    return sorted(vals)[len(vals) // 2] if vals else None


def typical_departure(plate, mock_day):
    """取该车参照天出发时刻的中位数时间(H:M:S)，套到 mock 日"""
    times = []
    for d, df in ref.items():
        r = df[df["vehicle_plate_number"] == plate]
        if len(r):
            t = pd.to_datetime(r.iloc[0]["departure_time"], errors="coerce")
            if pd.notna(t):
                times.append(t)
    if not times:
        return pd.Timestamp(f"{mock_day} 08:00:00")
    times.sort()
    t = times[len(times) // 2]
    return pd.Timestamp(f"{mock_day} {t.strftime('%H:%M:%S')}")


def most_common(plate, col):
    vals = []
    for d, df in ref.items():
        r = df[df["vehicle_plate_number"] == plate]
        if len(r):
            v = r.iloc[0][col]
            if pd.notna(v):
                vals.append(str(v))
    if not vals:
        return None
    return max(set(vals), key=vals.count)


# ---------- top-87 车牌（跨天出现最多） ----------
from collections import defaultdict
appear = defaultdict(set)
for d, df in ref.items():
    for p in df["vehicle_plate_number"].dropna():
        appear[p].add(d)
plates = [p for p, _ in sorted(appear.items(), key=lambda kv: -len(kv[1]))[:TARGET_ROWS]]
print(f"选用车牌 {len(plates)} 辆")


# ---------- es_vehicle_id 与车牌一一对应（取众数，撞号则分配唯一新号） ----------
def build_plate_eid_map():
    mode = {}
    for p in plates:
        vals = []
        for d, df in ref.items():
            r = df[df["vehicle_plate_number"] == p]
            if len(r):
                v = decode_es_vehicle_id(r.iloc[0]["es_vehicle_id"])
                if v is not None:
                    vals.append(v)
        if vals:
            mode[p] = max(set(vals), key=vals.count)
    used = set()
    nxt = max([v for v in mode.values() if v is not None], default=0) + 1
    out = {}
    for p in plates:
        v = mode.get(p)
        if v is None:
            out[p] = nxt
            nxt += 1
        elif v in used:
            while nxt in used:
                nxt += 1
            out[p] = nxt
            nxt += 1
        else:
            out[p] = v
            used.add(v)
    return out


PLATE_EID = build_plate_eid_map()
collisions = len(PLATE_EID) - len(set(PLATE_EID.values()))
print(f"es_vehicle_id 唯一性: {len(set(PLATE_EID.values()))} 唯一 / {len(PLATE_EID)} 车 (修正撞号 {collisions})")


# ---------- 生成 ----------
def build_sheet(mock_day):
    # 每天独立随机种子：同一天可复现，两天数值有日间差异
    random.seed(sum(ord(c) for c in mock_day))
    rows = []
    for plate in plates:
        eid = PLATE_EID[plate]
        org = most_common(plate, "organization_info_id")
        base_total = median_of(plate, "total_travel_distance") or 0.0
        base_actual = median_of(plate, "actual_work_distance") or 0.0
        base_dur = median_of(plate, "actual_work_duration") or 0
        base_anomaly = median_of(plate, "anomaly_event_count") or 0

        # 日间波动（大差不差，±10~20%）
        total = base_total * random.uniform(0.85, 1.15)
        actual = base_actual * random.uniform(0.8, 1.2)
        actual = min(actual, total)  # actual ≤ total
        rate = round(actual / total, 2) if total > 0 else 0.0
        dur = int(base_dur * random.uniform(0.85, 1.15))
        anomaly = max(0, int(round(base_anomaly + random.uniform(-0.5, 0.5))))

        dep = typical_departure(plate, mock_day)
        dep = dep + pd.Timedelta(minutes=random.randint(-30, 30))  # 出发时刻小幅浮动
        arr = dep + pd.Timedelta(seconds=dur)
        add = pd.Timestamp(f"{mock_day} 12:10:07")
        upd = pd.Timestamp(f"{mock_day} 20:10:07")
        rows.append({
            "id": str(gen_id()),
            "organization_info_id": str(org) if org else None,
            "es_vehicle_id": str(eid),
            "vehicle_plate_number": plate,
            "record_date": pd.Timestamp(f"{mock_day} 00:00:00"),
            "total_work_distance": round(total, 2),
            "total_travel_distance": round(total, 2),
            "actual_work_distance": round(actual, 2),
            "work_completion_rate": rate,
            "actual_work_duration": int(dur),
            "anomaly_event_count": anomaly,
            "departure_time": dep,
            "arrival_time": arr,
            "project_id": None,
            "add_time": add,
            "update_time": upd,
            "deleted": 0,
        })
    return pd.DataFrame(rows, columns=[
        "id", "organization_info_id", "es_vehicle_id", "vehicle_plate_number", "record_date",
        "total_work_distance", "total_travel_distance", "actual_work_distance",
        "work_completion_rate", "actual_work_duration", "anomaly_event_count",
        "departure_time", "arrival_time", "project_id", "add_time", "update_time", "deleted",
    ])


sheets = {d: build_sheet(d) for d in MOCK_DAYS}
sheet_map = {"08-04": sheets["2026-08-04"], "08-07": sheets["2026-08-07"]}
with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    for name, df in sheet_map.items():
        df.to_excel(writer, sheet_name=name, index=False)
print(f"已写出 {OUT}: 08-04={len(sheet_map['08-04'])} 行, 08-07={len(sheet_map['08-07'])} 行")


# ---------- 自检 ----------
def check(df, name):
    ok = True
    n = len(df)
    if n != TARGET_ROWS:
        print(f"  [✗] {name} 行数 {n} != {TARGET_ROWS}")
        ok = False
    r = (pd.to_numeric(df["work_completion_rate"], errors="coerce").round(2) ==
         (pd.to_numeric(df["actual_work_distance"]) / pd.to_numeric(df["total_travel_distance"])).round(2))
    if not r.all():
        print(f"  [✗] {name} rate 公式不符 {n - r.sum()} 行")
        ok = False
    dur = pd.to_numeric(df["actual_work_duration"], errors="coerce")
    diff = (pd.to_datetime(df["arrival_time"]) - pd.to_datetime(df["departure_time"])).dt.total_seconds()
    if not (dur == diff).all():
        print(f"  [✗] {name} duration 公式不符 {(dur != diff).sum()} 行")
        ok = False
    if df["update_time"].isna().any():
        print(f"  [✗] {name} update_time 有空值")
        ok = False
    if df["es_vehicle_id"].duplicated().any():
        print(f"  [✗] {name} es_vehicle_id 重复")
        ok = False
    if df["id"].duplicated().any():
        print(f"  [✗] {name} id 重复")
        ok = False
    print(f"  [{'✓' if ok else '✗'}] {name}: {n} 行, 公式/唯一性/update_time 全部通过" if ok else f"  [{name} 自检失败]")


for d, df in sheets.items():
    check(df, d)
