import json
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
def get_sort():
    path = "rules.json"
    sort = None
    try:
        with open(path,"r",encoding="utf-8") as f:
            sort = json.load(f)
    except FileNotFoundError:
        logger.exception("json文件不存在,是不是执行程序的文件夹不对,或者没有创建")
    except json.JSONDecodeError:
        logger.exception("json的格式不对,请检查一下")
        return sort
    return sort
def scan_dir():
    ext_dict = {}
    while True:
        raw = input("请输入文件夹路径：")
        raw = raw.strip()
        raw = raw.strip('"')
        raw = raw.strip("'")
        p = Path(raw).expanduser()
        if not p.is_dir():
            print("这个路径不存在或不是文件夹，请重新输入:")
            continue
        if not any(p.iterdir()):
            print("这个文件夹是空的，请重新输入要整理的文件夹:")
            continue
        for file in p.iterdir():
            if file.is_file():
                ext = file.suffix if file.suffix else "（无扩展名）"
                ext_dict.setdefault(ext, []).append(file.name)
        return ext_dict    
def classify():
    file_sort = scan_dir()
    sort = get_sort()
    if not sort:
        logger.error("读取json文件,返回值为空,检查一下是不是没有创建json文件,或者格式有错")
        return None
    count = {"image":0,"documents":0,"videos":0,"music":0,"others":0}
    for ext, files in file_sort.items():
        if ext in sort["images"]:
            count["image"] += len(files)
        elif ext in sort["documents"]:
            count["documents"] += len(files)
        elif ext in sort["videos"]:
            count["videos"] += len(files)
        elif ext in sort["music"]:
            count["music"] += len(files)
        else:
            count["others"] += len(files)
    return count
if __name__ == "__main__":
    count = classify()
    print(count)