import asyncio
import csv
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import aiohttp
AMAP_KEY = os.getenv("AMAP_KEY", "4d628e660688eb29a50df9f9a8bfe71d")
KEYWORDS = [
    "废品回收",
    "再生资源回收",
    "旧货回收",
    "回收站",
]
QPS = 2
OUTPUT_DIR = "output"
PROGRESS_FILE = os.path.join(OUTPUT_DIR, ".progress.json")
DATA_FILE = os.path.join(OUTPUT_DIR, ".data.json")
AMAP_BASE = "https://restapi.amap.com/v3"
#令牌桶
class RateLimiter:
    def __init__(self, max_per_second: float = 3):
        self.max_per_second = max_per_second
        self._tokens = float(max_per_second)
        self._updated_at = time.monotonic()
        self._lock = asyncio.Lock()
    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._updated_at
            self._tokens = min(self.max_per_second, self._tokens + elapsed * self.max_per_second)
            self._updated_at = now
            if self._tokens < 1:
                wait = (1 - self._tokens) / self.max_per_second
                await asyncio.sleep(wait)
                self._tokens = 0
                self._updated_at = time.monotonic()
            else:
                self._tokens -= 1
class QuotaExceededError(Exception):
    """API 调用额度超限"""
    pass
# 高德 API 客户端
class AmapClient:
    def __init__(self, key: str, session: aiohttp.ClientSession, limiter: RateLimiter):
        self._key = key
        self._session = session
        self._limiter = limiter

    async def _request(self, api: str, params: dict) -> Optional[dict]:
        params["key"] = self._key
        await self._limiter.acquire()
        try:
            async with self._session.get(f"{AMAP_BASE}{api}", params=params, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                if data.get("status") != "1":
                    info = data.get("info", "")
                    infocode = data.get("infocode", "")
                    limit_errs = {"DAILY_QUERY_OVER_LIMIT", "USER_DAILY_QUERY_OVER_LIMIT", "INSUFFICIENT_PRIVILEGES", "QPS_HAS_EXCEEDED_THE_LIMIT", "CUQPS_HAS_EXCEEDED_THE_LIMIT", "10003", "10008", "10009", "10010", "10011"}
                    if info in limit_errs or infocode in limit_errs:
                        raise QuotaExceededError(info)
                    print(f"  [WARN] API 返回异常: {api} {params} → {info}")
                    return None
                return data
        except QuotaExceededError:
            raise
        except Exception as e:
            print(f"  [ERROR] 请求失败: {api} {params} → {e}")
            return None

    async def get_districts(self) -> list[dict]:
        data = await self._request("/config/district", {
            "keywords": "中国",
            "subdistrict": "3",
            "extensions": "base",
        })
        if not data:
            return []
        dists = data.get("districts", [])
        return dists[0].get("districts", []) if dists else []
    async def search_poi(self, keyword: str, city_adcode: str, page: int = 1) -> Optional[dict]:
        """搜索 POI"""
        return await self._request("/place/text", {
            "keywords": keyword,
            "city": city_adcode,
            "offset": "25",
            "page": str(page),
        })
# 区县统计数据
@dataclass
class DistrictStats:
    province: str = ""
    province_code: str = ""
    city: str = ""
    city_code: str = ""
    district: str = ""
    district_code: str = ""
    keyword_counts: dict = field(default_factory=lambda: {k: set() for k in KEYWORDS})
    all_pois: set = field(default_factory=set)

    @property
    def total(self) -> int:
        return len(self.all_pois)

# POI 去重（(poi_id, name, address) 三元组）
def poi_key(poi: dict) -> tuple:
    return (poi.get("id", ""), poi.get("name", ""), poi.get("address", ""))


#遍历行政区划并搜索
def flatten_districts(provinces: list[dict]) -> list[tuple]:
    """展开省市区县三级列表"""
    rows = []
    for prov in provinces:
        pname = prov.get("name", "")
        pcode = prov.get("adcode", "")
        for city in prov.get("districts", []):
            cname = city.get("name", "")
            ccode = city.get("adcode", "")
            city_districts = city.get("districts", [])
            if not city_districts:
                rows.append((pname, pcode, cname, ccode, cname, ccode))
            else:
                for dist in city_districts:
                    dname = dist.get("name", "")
                    dcode = dist.get("adcode", "")
                    rows.append((pname, pcode, cname, ccode, dname, dcode))
    return rows


async def search_district(client: AmapClient, row: tuple) -> Optional[DistrictStats]:
    """一个区县的所有关键词执行搜索"""
    province, province_code, city, city_code, district, district_code = row
    print(f"  [{province}] {city} {district} ({district_code})")
    
    stats = DistrictStats(
        province=province,
        province_code=province_code,
        city=city,
        city_code=city_code,
        district=district,
        district_code=district_code,
    )

    for kw in KEYWORDS:
        page = 1
        total = 0
        while True:
            resp = await client.search_poi(kw, district_code, page)
            if resp is None:
                break
            pois = resp.get("pois", [])
            total = int(resp.get("count", 0))
            if not pois:
                break
            for poi in pois:
                key = poi_key(poi)
                stats.keyword_counts[kw].add(key)
                stats.all_pois.add(key)
            if page * 25 >= total:
                break
            page += 1

    return stats
# 输出
def export_csv(stats_list: list[DistrictStats], path: str):
    """导出 CSV """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    headers = ["省", "省code", "市", "市code", "区县", "区县code"] + KEYWORDS + ["总计"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for s in stats_list:
            row = [
                s.province, s.province_code,
                s.city, s.city_code,
                s.district, s.district_code,
            ]
            row.extend(len(s.keyword_counts[k]) for k in KEYWORDS)
            row.append(s.total)
            w.writerow(row)
    print(f"\n[OK] CSV 已导出: {path}")


def export_html(stats_list: list[DistrictStats], path: str):
    """导出热力色标HTML 表格"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    max_total = max((s.total for s in stats_list), default=1)

    def color(total: int) -> str:
        if total == 0:
            return "#f0f0f0"
        ratio = total / max_total
        if ratio < 0.05:
            return "#ffffcc"
        elif ratio < 0.15:
            return "#ffeda0"
        elif ratio < 0.3:
            return "#feb24c"
        elif ratio < 0.5:
            return "#fd8d3c"
        else:
            return "#e31a1c"

    rows_html = ""
    for s in stats_list:
        bg = color(s.total)
        kw_cells = "".join(f'<td style="text-align:right">{len(s.keyword_counts[k])}</td>' for k in KEYWORDS)
        rows_html += (
            f"<tr style='background:{bg}'>"
            f"<td>{s.province}</td><td>{s.province_code}</td>"
            f"<td>{s.city}</td><td>{s.city_code}</td>"
            f"<td>{s.district}</td><td>{s.district_code}</td>"
            f"{kw_cells}"
            f"<td style='text-align:right;font-weight:bold'>{s.total}</td>"
            f"</tr>\n"
        )

    kw_headers = "".join(f"<th>{k}</th>" for k in KEYWORDS)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>再生资源回收行业竞品统计</title>
<style>
body {{ font-family: sans-serif; margin: 20px; }}
table {{ border-collapse: collapse; font-size: 13px; }}
th, td {{ border: 1px solid #ccc; padding: 4px 8px; white-space: nowrap; }}
th {{ background: #333; color: #fff; position: sticky; top: 0; }}
tr:hover {{ opacity: 0.85; }}
</style>
</head>
<body>
<h2>再生资源回收行业竞品区域统计</h2>
<p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p>色标: 从白 → 黄 → 橙 → 红 (数量越多颜色越深)</p>
<table>
<thead><tr>
<th>省</th><th>省code</th><th>市</th><th>市code</th><th>区县</th><th>区县code</th>
{kw_headers}
<th>总计</th>
</tr></thead>
<tbody>
{rows_html}
</tbody>
</table>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML 已导出: {path}")

# 断点续跑（保存/恢复进度）
def save_progress(completed_codes: set):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({"completed": list(completed_codes)}, f, ensure_ascii=False)


def load_progress() -> set:
    if not os.path.exists(PROGRESS_FILE):
        return set()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("completed", []))
    except (json.JSONDecodeError, KeyError):
        return set()


def stats_to_dict(s: DistrictStats) -> dict:
    return {
        "province": s.province,
        "province_code": s.province_code,
        "city": s.city,
        "city_code": s.city_code,
        "district": s.district,
        "district_code": s.district_code,
        "keyword_counts": {k: list(v) for k, v in s.keyword_counts.items()},
        "all_pois": list(s.all_pois),
    }


def dict_to_stats(d: dict) -> DistrictStats:
    s = DistrictStats(
        province=d["province"],
        province_code=d["province_code"],
        city=d["city"],
        city_code=d["city_code"],
        district=d["district"],
        district_code=d["district_code"],
    )
    s.keyword_counts = {k: set(v) for k, v in d["keyword_counts"].items()}
    s.all_pois = set(tuple(x) for x in d["all_pois"])
    return s


def save_data(stats_list: list[DistrictStats]):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([stats_to_dict(s) for s in stats_list], f, ensure_ascii=False)


def load_data() -> list[DistrictStats]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return [dict_to_stats(d) for d in json.load(f)]
    except (json.JSONDecodeError, KeyError):
        return []
# 主入口
async def main():
    if AMAP_KEY == "YOUR_AMAP_KEY_HERE":
        print("=" * 60)
        print("请先设置高德 Web 服务 Key：")
        print("=" * 60)
        sys.exit(1)

    limiter = RateLimiter(max_per_second=QPS)
    async with aiohttp.ClientSession() as session:
        client = AmapClient(AMAP_KEY, session, limiter)

        # 1) 获取行政区划
        print("[1/4] 获取全国行政区划...")
        provinces = await client.get_districts()
        if not provinces:
            print("[ERROR] 无法获取行政区划数据，请检查 Key 是否有效")
            return

        districts = flatten_districts(provinces)
        print(f"  省: {len(provinces)}, 地市: {len(set(r[2] for r in districts))}, 区县: {len(districts)}")

        # 2) （断点续跑）
        completed = load_progress()
        all_stats = load_data()
        print(f"\n[2/4] 开始搜索 {len(districts)} 个区县 × {len(KEYWORDS)} 个关键词...")
        if completed:
            print(f"  之前已完成 {len(completed)} 个区县，跳过直接继续")

        try:
            for i, row in enumerate(districts, 1):
                district_code = row[5]
                if district_code in completed:
                    continue
                stats = await search_district(client, row)
                if stats:
                    all_stats.append(stats)
                    completed.add(district_code)
                if i % 50 == 0:
                    save_progress(completed)
                    save_data(all_stats)
                    print(f"  进度: {i}/{len(districts)} 区县 (已保存)")
        except QuotaExceededError as e:
            save_progress(completed)
            save_data(all_stats)
            print(f"\n[!] 额度已超限 ({e})，已采集 {len(all_stats)} 个区县，进度已保存")
            print("    - 明天再跑会自动跳过已完成的区县")

        # 3) 保存最终进度
        save_progress(completed)
        save_data(all_stats)

        # 4) 汇总
        print(f"\n[3/4] 数据汇总...")
        all_stats.sort(key=lambda s: s.total, reverse=True)

        # 打印 Top 20
        print("\n--- 竞品最多的 Top 20 区县 ---")
        print(f"{'排名':>4} {'省':8} {'市':10} {'区县':8} {'总计':>6}")
        for idx, s in enumerate(all_stats[:20], 1):
            print(f"{idx:>4} {s.province:8} {s.city:10} {s.district:8} {s.total:>6}")

        # 5) 导出
        print(f"\n[4/4] 导出结果...")
        export_csv(all_stats, os.path.join(OUTPUT_DIR, "recycle_stats.csv"))
        export_html(all_stats, os.path.join(OUTPUT_DIR, "recycle_heatmap.html"))

        # 6) 对无竞品的区县单独输出
        zero = [s for s in all_stats if s.total == 0]
        print(f"\n无竞品的区县: {len(zero)} 个")
        if zero:
            with open(os.path.join(OUTPUT_DIR, "no_competition_districts.csv"), "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["省", "省code", "市", "市code", "区县", "区县code"])
                for s in zero:
                    w.writerow([s.province, s.province_code, s.city, s.city_code, s.district, s.district_code])
            print(f"  已导出: {os.path.join(OUTPUT_DIR, 'no_competition_districts.csv')}")

    print(f"\n[完成] 共扫描 {len(all_stats)} 个区县")
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
