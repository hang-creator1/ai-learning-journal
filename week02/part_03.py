try:
    import requests
except ImportError:
    print("requests 未安装，在终端运行: pip install requests")
print(f"当前request的版本为: {requests.__version__}")
url = "https://air-quality-api.open-meteo.com/v1/air-quality999"
def get_air_quality(lat,lon):
    params = {"latitude":lat,"longitude":lon,"current":"us_aqi,pm2_5"}
    try:
        resp = requests.get(url,params,timeout=0.001)
        resp.raise_for_status()
        print(f"实际请求的完整地址: {resp.url}")
        # raise_for_status 已保证：能走到这必然 2xx，无需再 if status_code == 200
        data = resp.json().get("current")
        if not data:
            return None
        us_aqi = data["us_aqi"]
        pm2_5 = data["pm2_5"]
        result = (us_aqi, pm2_5)
    except requests.exceptions.Timeout:
        print("请求超时了，检查一下网络")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求出异常了（可能没联网）: {e}")
        return None
    return result
def aqi_level(CITIES):
    result = []
    for name,lat,lon in CITIES:
        get_result = {}
        level = ""
        get_result["城市"] = name
        data = get_air_quality(lat,lon)
        if not data:                                  
            result.append({"城市": name, "失败": True})
            continue
        us_aqi,pm2_5 = data
        get_result["AQI"] = us_aqi
        get_result["PM2.5"] = pm2_5
        if us_aqi <= 50:
            level = "优"
        elif us_aqi <= 100:
            level = "良"
        elif us_aqi <= 150:
            level = "轻度污染"
        elif us_aqi <= 200:
            level = "中度污染"
        else:
            level = "重度污染"
        get_result["等级"] = level
        result.append(get_result)
    return result
if __name__ == "__main__":
    CITIES = [
        ("北京", 39.9, 116.4),
        ("上海", 31.2, 121.5),
        ("广州", 23.1, 113.3),
    ]
    result = aqi_level(CITIES)
    has_data = False
    for a in result:
        if not a.get("失败"):
            has_data = True
    if has_data:
        print(f"{'城市':<8}{'AQI':<8}{'PM2.5':<8}{'等级':<8}")
    for x in result:
        if x.get("失败"):
            print(f"{x['城市']}查询失败")
        else:
            print(f"{x['城市']:<8}{x['AQI']:<8}{x['PM2.5']:<8}{x['等级']:<8}")