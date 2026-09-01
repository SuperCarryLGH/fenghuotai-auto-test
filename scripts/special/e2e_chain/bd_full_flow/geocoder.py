"""
高德地图地理编码模块
功能：
1. 地址 → 城市/区县编码
2. 地址 → 经纬度
"""
import os
import json
import time
import requests

# 高德 API Key
AMAP_KEY = "ea44abcc66c996667953325792c84c8f"
AMAP_BASE = "https://restapi.amap.com/v3"

# 缓存文件路径
CACHE_FILE = os.path.join(os.path.dirname(__file__), "geocache.json")

# 限流：每秒最多3次请求
_last_request_time = 0
REQUEST_INTERVAL = 0.35


def _load_cache():
    """加载缓存"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache):
    """保存缓存"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def _rate_limit():
    """限流控制"""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    _last_request_time = time.time()


def geocode_address(address, province="", city="", district=""):
    """
    地理编码：将地址转换为坐标和行政区划编码
    
    参数:
        address: 详细地址
        province: 省份
        city: 城市
        district: 区县
    
    返回:
        {
            "province_code": "330000",
            "city_code": "330100",
            "district_code": "330108",
            "lat": 30.2085,
            "lon": 120.212
        }
    """
    # 检查缓存
    cache_key = f"{province}{city}{district}{address}"
    cache = _load_cache()
    if cache_key in cache:
        return cache[cache_key]
    
    # 构造地址
    full_address = f"{province}{city}{district}{address}"
    
    # 限流
    _rate_limit()
    
    try:
        resp = requests.get(
            f"{AMAP_BASE}/geocode/geo",
            params={
                "key": AMAP_KEY,
                "address": full_address,
                "output": "json",
            },
            timeout=10,
        )
        data = resp.json()
        
        if data.get("status") == "1" and data.get("geocodes"):
            geocode = data["geocodes"][0]
            
            # 解析行政区划编码
            adcode = geocode.get("adcode", "")
            province_code = adcode[:2] + "0000" if len(adcode) >= 6 else ""
            city_code = adcode[:4] + "00" if len(adcode) >= 6 else ""
            district_code = adcode if len(adcode) == 6 else ""
            
            # 解析坐标
            location = geocode.get("location", "")
            lat, lon = 0, 0
            if location:
                parts = location.split(",")
                if len(parts) == 2:
                    lat = float(parts[1])  # 纬度
                    lon = float(parts[0])  # 经度
            
            result = {
                "province_code": province_code,
                "city_code": city_code,
                "district_code": district_code,
                "lat": lat,
                "lon": lon,
                "adcode": adcode,
                "formatted_address": geocode.get("formatted_address", ""),
            }
            
            # 保存缓存
            cache[cache_key] = result
            _save_cache(cache)
            
            return result
        
        return {
            "province_code": "",
            "city_code": "",
            "district_code": "",
            "lat": 0,
            "lon": 0,
        }
    
    except Exception as e:
        print(f"  ⚠️ 地理编码失败: {e}")
        return {
            "province_code": "",
            "city_code": "",
            "district_code": "",
            "lat": 0,
            "lon": 0,
        }


def batch_geocode(addresses):
    """
    批量地理编码
    
    参数:
        addresses: [{"province": "", "city": "", "district": "", "address": ""}, ...]
    
    返回:
        [{"province_code": "", "city_code": "", "district_code": "", "lat": 0, "lon": 0}, ...]
    """
    results = []
    for addr in addresses:
        result = geocode_address(
            addr.get("address", ""),
            addr.get("province", ""),
            addr.get("city", ""),
            addr.get("district", ""),
        )
        results.append(result)
    return results


# 测试
if __name__ == "__main__":
    result = geocode_address("浙江省杭州市滨江区网商路599号", "浙江省", "杭州市", "滨江区")
    print(json.dumps(result, ensure_ascii=False, indent=2))
