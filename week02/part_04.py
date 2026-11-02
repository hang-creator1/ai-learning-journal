import json
def parse(raw):
    result = json.loads(raw)
    return result
def worst_city(raw):
    data = parse(raw)
    max = data[0]["aqi"]
    city_name = data[0]["city"]
    for x in data:
        if x["aqi"] > max:
            city_name = x["city"]
    return city_name
def save(raw):
    data = parse(raw)
    pro_data = []
    for x in data:
        pro_dict = {}
        pro_dict["城市"] = x["city"]
        pro_dict["AQI"] = x["aqi"]
        pro_data.append(pro_dict)
    path = "air.json"
    with open(path,"w",encoding="utf-8") as f:
        json.dump(pro_data,f, ensure_ascii=False, indent=2)
def read_history():
    path = "air.json"
    try:
        with open(path,"r",encoding="utf-8") as f:
            result = json.load(f)
            return result
    except FileNotFoundError:
        print("还没有缓存")
        return None
if __name__ == "__main__":
    RAW = '[{"city": "北京", "aqi": 55}, {"city": "上海", "aqi": 88}, {"city": "广州", "aqi": 43}, {"city": "成都", "aqi": 120}]'
    result = parse(RAW)
    print(type(result))
    result1 = worst_city(RAW)
    print(result1)
    save(RAW)
    result2 = read_history()
    print(result2)
