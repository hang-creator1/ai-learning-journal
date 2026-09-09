import logging
import os
logger = logging.getLogger(__name__)
try:
    import requests
except ImportError:
    logger.exception("requests 未安装，在终端运行: pip install requests")
    logger.debug(f"当前request的版本为: {requests.__version__}")
log_file = "air.log"
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s %(name)s [%(levelname)s] %(message)s",
    handlers = [
        logging.FileHandler(log_file,encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force = True,
)
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
def get_air_quality(lat,lon):
    params = {"latitude":lat,"longitude":lon,"current":"us_aqi,pm2_5,"}
    try:
        resp = requests.get(url,params,timeout=10)
        resp.raise_for_status()
        logger.debug(f"实际请求的完整地址: {resp.url}")
        data = resp.json().get("current")
        if not data:
            return None
        us_aqi = data["us_aqi"]
        pm2_5 = data["pm2_5"]
        result = (us_aqi, pm2_5)
    except requests.exceptions.Timeout:
        print("请求超时了，检查一下网络")
        logger.error("请求超时了,看看是不是timeout的问题")
        return None
    except requests.exceptions.RequestException:
        print(f"请求出异常了（可能没联网）")
        logger.exception("请求出现了异常")
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
        try:
            us_aqi,pm2_5,learn = data
            get_result["LEARN"] = learn
            get_result["AQI"] = us_aqi
            get_result["PM2.5"] = pm2_5
        except ValueError:
            logger.exception("出现了错误,关于变量的")
            result.append({"城市": name, "失败": True})
            continue
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
    logger.info("参数是:%s",CITIES)
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
    for b in logging.root.handlers[:]:
        b.close()
        logging.root.removeHandler(b)
    #os.remove(log_file)