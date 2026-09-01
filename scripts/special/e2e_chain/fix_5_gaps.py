"""
补建 4 条真缺口站点（秀峰里座机号除外）
流程: 登录BD → 建线索(清洗后电话, stationType=3, belongCenterId) → 领取 → 签约 → 校验
按 run_all.py 逻辑, type=31, minWeight=50, 价格取文档
"""
import sys, os, time, json, requests
import pymysql

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FLOW_DIR = os.path.join(PROJECT_ROOT, 'scripts/special/e2e_chain/bd_full_flow')
sys.path.insert(0, FLOW_DIR)

import importlib.util
def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

cfg = load_mod("flow_config", os.path.join(FLOW_DIR, "config.py"))
geo_mod = load_mod("geocoder", os.path.join(FLOW_DIR, "geocoder.py"))
geocode_address = geo_mod.geocode_address
COMMON_HEADERS, PROVINCE_CODE_MAP, INDUSTRY_MAP, APP_URL = cfg.COMMON_HEADERS, cfg.PROVINCE_CODE_MAP, cfg.INDUSTRY_MAP, cfg.API_BASE_URL

RECORDS = [
    {"stationName":"阳光星城外包店","contactName":"周鹏","contactPhone":"13175316020",
     "industry":"快递驿站","recyclePrice":0.7,"clearPrice":1.2,
     "province":"浙江省","city":"台州","district":"玉环市","street":"玉城街道",
     "detailAddress":"浙江省台州市玉环市阳光星城南门商铺83号顺丰驿站","bdPhone":"13606651729","bdName":"冯利民",
     "centerId":"2069365345938698241"},
    {"stationName":"金宁街废品废品回收李","contactName":"李老板","contactPhone":"19143700284",
     "industry":"废品回收站","recyclePrice":0.8,"clearPrice":1.2,
     "province":"江苏省","city":"南京市","district":"江宁","street":"横溪街道",
     "detailAddress":"南京市江宁区横溪街道金宁街118号","bdPhone":"17342701205","bdName":"杜泽旭",
     "centerId":"2071977701136384001"},
    {"stationName":"小贺废品回收","contactName":"曹贺","contactPhone":"17053384000",
     "industry":"废品回收站","recyclePrice":0.5,"clearPrice":1.2,
     "province":"浙江省","city":"杭州市","district":"上城区","street":"九堡街道",
     "detailAddress":"多立方11幢112号","bdPhone":"13386852617","bdName":"高尚",
     "centerId":"2093893676013428737"},
    {"stationName":"快递驿站-皇嘉锦苑369","contactName":"柏光琴","contactPhone":"15956994369",
     "industry":"快递驿站","recyclePrice":1.2,"clearPrice":1.6,
     "province":"安徽省","city":"合肥市","district":"蜀山区","street":"小庙镇",
     "detailAddress":"安徽省合肥市蜀山区小庙镇兆勋路建邦·皇嘉锦苑","bdPhone":"15056572360","bdName":"唐家林",
     "centerId":"2071978918246195201"},
]

def get_db():
    return pymysql.connect(host='rm-bp1kmprsfdog024fsro.mysql.rds.aliyuncs.com', port=3306,
        user='sf_fht_dev', password=os.getenv('DB_PASSWORD','8HUvyZf6X&FNR%5'),
        database='fht_yhs', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=5)

def login(mobile):
    try:
        r = requests.post(f"{APP_URL}/admin-api/system/auth/sms-login",
            json={"mobile": mobile, "code": "9999"}, headers=COMMON_HEADERS, timeout=10)
        d = r.json()
        return d["data"]["accessToken"] if d.get("code") == 0 else None
    except Exception as e:
        print(f"  登录异常: {e}"); return None

def find_clue(phone):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT id, status, belong_center_id FROM station_clue WHERE contact_phone=%s AND deleted=0', (phone,))
        row = cur.fetchone()
    db.close()
    return row

def create_clue(token, rec):
    h = COMMON_HEADERS.copy(); h["Authorization"] = f"Bearer {token}"
    detail_address = rec["detailAddress"]
    geo = geocode_address(detail_address, rec["province"], rec["city"], rec["district"])
    body = {
        "poolType": 0,
        "clueName": rec["stationName"], "contactName": rec["contactName"], "contactPhone": rec["contactPhone"],
        "stationType": 3, "detailAddress": detail_address,
        "province": rec["province"], "provinceCode": geo.get("province_code") or PROVINCE_CODE_MAP.get(rec["province"], "330000"),
        "city": rec["city"], "cityCode": geo.get("city_code") or "331000",
        "district": rec["district"], "districtCode": geo.get("district_code") or "330108",
        "lat": geo.get("lat", 0), "lon": geo.get("lon", 0),
        "belongCenterId": rec["centerId"],
    }
    for attempt in range(3):
        try:
            r = requests.post(f"{APP_URL}/admin-api/recycle/station-clue/create", json=body, headers=h, timeout=15)
            d = r.json()
            if d.get("code") == 0:
                return d["data"]
            print(f"  建线索失败(code={d.get('code')}): {d.get('msg','')} 重试{attempt+1}")
        except Exception as e:
            print(f"  建线索异常: {e} 重试{attempt+1}")
        time.sleep(2)
    return None

def claim_clue(token, clue_id):
    h = COMMON_HEADERS.copy(); h["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(f"{APP_URL}/admin-api/recycle/station-clue/claim?id={clue_id}", headers=h, timeout=10)
        return r.json()
    except Exception as e:
        return {"code": -1, "msg": str(e)}

def sign(token, clue_id, rec):
    h = COMMON_HEADERS.copy(); h["Authorization"] = f"Bearer {token}"
    ind = INDUSTRY_MAP.get(rec["industry"], INDUSTRY_MAP["默认"])
    geo = geocode_address(rec["detailAddress"], rec["province"], rec["city"], rec["district"])
    body = {"clueId": clue_id, "type": 31,
        "industry": ind["value"], "industryKey": ind["key"], "operationMode": "自营",
        "recyclePrice": rec["recyclePrice"], "clearPrice": rec["clearPrice"],
        "stationName": rec["stationName"], "contactName": rec["contactName"], "contactPhone": rec["contactPhone"],
        "province": rec["province"], "provinceCode": geo.get("province_code") or PROVINCE_CODE_MAP.get(rec["province"], "330000"),
        "city": rec["city"], "district": rec["district"], "street": rec["street"],
        "detailAddress": rec["detailAddress"], "lat": geo.get("lat", 0), "lon": geo.get("lon", 0),
        "paymentType": 10, "cleartMode": 10, "callMode": 10, "minWeight": 50,
        "settlementType": 10, "incomeType": 1, "invoiceType": 1, "withdrawType": 1}
    for attempt in range(3):
        try:
            r = requests.post(f"{APP_URL}/admin-api/recycle/station-clue/sign-submit", json=body, headers=h, timeout=30)
            d = r.json()
            if d.get("code") == 0:
                return d
            if "重复请求" in str(d.get("msg","")):
                time.sleep(5); continue
            print(f"  签约失败(code={d.get('code')}): {d.get('msg','')} 重试{attempt+1}")
        except Exception as e:
            print(f"  签约异常: {e} 重试{attempt+1}")
        time.sleep(3)
    return None

def verify_station(phone):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, name, type, status, industry, town, recycle_price, clear_price, manager_phone, min_weight, lat, lon, virtual_user_id FROM station WHERE manager_phone=%s AND deleted=0", (phone,))
        row = cur.fetchone()
    db.close()
    return row

def main():
    results = []
    for rec in RECORDS:
        print(f"\n{'='*55}\n处理: {rec['stationName']} 电话={rec['contactPhone']} BD={rec['bdName']}({rec['bdPhone']})")
        token = login(rec["bdPhone"])
        if not token:
            print("  ❌ BD登录失败"); results.append({"station":rec["stationName"],"result":"BD登录失败"}); continue
        clue = find_clue(rec["contactPhone"])
        if clue:
            clue_id = clue["id"]
            print(f"  已有活跃线索 #{clue_id} status={clue['status']}")
            if clue["status"] == 41:
                st = verify_station(rec["contactPhone"])
                print(f"  已签约. 站点: {st['id']} {st['name']}" if st else "  已签约但站点缺失!")
                results.append({"station":rec["stationName"],"result":"已存在","stationId":st['id'] if st else None}); continue
            if clue["status"] == 10:
                r = claim_clue(token, clue_id)
                print(f"  领取: code={r.get('code')} {r.get('msg','')}")
                time.sleep(1)
        else:
            clue_id = create_clue(token, rec)
            if not clue_id:
                print("  ❌ 建线索失败, 跳过"); results.append({"station":rec["stationName"],"result":"建线索失败"}); continue
            print(f"  ✅ 线索创建成功 clue_id={clue_id}")
            time.sleep(1)
            r = claim_clue(token, clue_id)
            print(f"  领取: code={r.get('code')} {r.get('msg','')}")
            time.sleep(1)
        r = sign(token, clue_id, rec)
        if r and r.get("code") == 0:
            d = r.get("data", {})
            st = verify_station(rec["contactPhone"])
            ok = "✅" if st else "⚠️"
            print(f"  {ok} 签约成功 signId={d.get('signId')} stationId={d.get('stationId')}")
            if st:
                print(f"     站点校验: id={st['id']} name={st['name']} type={st['type']} status={st['status']} ind={st['industry']} 价={st['recycle_price']}/{st['clear_price']} minW={st['min_weight']}")
            results.append({"station":rec["stationName"],"result":"成功","signId":d.get("signId"),"stationId":d.get("stationId"),"verify":bool(st)})
        else:
            print("  ❌ 签约失败")
            results.append({"station":rec["stationName"],"result":"签约失败"})
        time.sleep(2)
    print(f"\n{'='*55}\n汇总:")
    for x in results: print(f"  {x}")
    with open('/Users/rs/Documents/fix_5_gaps_result.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()