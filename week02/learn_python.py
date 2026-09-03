# ============================================================
# Python 第二周进阶练习（完整版）
# 内容：异常处理 / 模块与包 / requests与HTTP API / JSON处理 /
#       类型标注 / logging日志 / .env密钥管理 / pytest测试 /
#       venv虚拟环境 / Git分支与合并
# 运行方式：在终端执行  python learn_python.py
# 每一行都可以问我，比如"第 30 行是什么意思"
#
# 与学习计划的对应关系：
#   一、异常处理 try/except          -> 第2周 周一
#   二、模块与包                     -> 第2周 周二
#   三、requests 与 HTTP API         -> 第2周 周二 / 周三
#   四、JSON 处理                    -> 第2周 周三
#   五、类型标注                     -> 第2周 周四
#   六、logging 日志                 -> 第2周 周四
#   七、.env 密钥管理                -> 第2周 周四
#   八、pytest 写第一个测试          -> 第2周 周四 / 周末实战
#   九、venv 虚拟环境                -> 第1周提到过但没练，补课
#   十、Git 分支 branch / 合并 merge -> 第2周 周五
# ============================================================

import json
import logging
import os
import sys


# ============================================================
# 一、异常处理（try / except / else / finally / raise）
# ============================================================

def demo_exception():
    print("=" * 50)
    print("一、异常处理")
    print("=" * 50)

    # --- 1. 最基本用法：try 里放可能出错的代码，except 接住错误 ---
    # 不接住的话，程序会直接崩溃报错；接住了就能继续往下跑
    try:
        n = int("abc")                 # "abc" 没法转成整数，会抛出 ValueError
    except ValueError as e:            # as e：把异常对象接住，e 里有错误信息
        print(f"抓到异常: {e}")

    # --- 2. 不同的错误分开处理：写多个 except ---
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:      # 除数为 0 的错误
            print("除数不能是 0！")
            return None
        except TypeError:              # 类型不对（比如传了字符串）的错误
            print("类型不对，没法相除！")
            return None

    print(f"10 / 2 = {safe_divide(10, 2)}")
    safe_divide(10, 0)
    safe_divide(10, "x")

    # --- 3. 多个异常写在一行（用元组），统一处理 ---
    try:
        data = [1, 2, 3]
        print(data[10])                # 下标越界，抛 IndexError
    except (IndexError, KeyError) as e:
        # type(e).__name__ 拿到异常类的名字字符串，比如 "IndexError"
        print(f"越界或键不存在: {type(e).__name__}")

    # --- 4. else 和 finally ---
    try:
        num = int("123")               # 这行不会出错
    except ValueError:
        print("转换失败")
    else:                              # else：try 里没出任何异常时才执行
        print(f"else 分支: 转换成功, num = {num}")
    finally:                           # finally：不管出没出异常一定执行，常用来收尾（关文件等）
        print("finally 分支: 无论如何都会执行")

    # --- 5. raise：主动抛出异常（自己发现问题，主动报错）---
    def set_age(age):
        if age < 0:
            raise ValueError(f"年龄不能是负数: {age}")
        return age

    try:
        set_age(-5)
    except ValueError as e:
        print(f"raise 演示: {e}")

    # --- 6. 自定义异常：写一个类继承 Exception 就行 ---
    class BalanceNotEnoughError(Exception):
        """自定义异常：余额不足时抛出"""
        pass

    try:
        raise BalanceNotEnoughError("余额只有 10 元，买不了 100 元的东西")
    except BalanceNotEnoughError as e:
        print(f"自定义异常: {e}")

    # --- 7. 常见异常速查表 ---
    print("""
常见异常速查:
  ValueError         值不对（如 int("abc")）
  TypeError          类型不对（如 "1" + 1）
  FileNotFoundError  文件不存在
  KeyError           字典里没有这个键
  IndexError         列表下标越界
  ZeroDivisionError  除数为 0
  ImportError        导入的模块不存在
""")


# ============================================================
# 二、模块与包（import 的各种用法）
# ============================================================

def demo_module():
    print("\n" + "=" * 50)
    print("二、模块与包")
    print("=" * 50)

    # --- 1. import 的几种写法 ---
    import math                        # 导入整个模块，用时写 math.sqrt()
    from math import pi                # 只从模块里拿一个东西，用时直接写 pi
    import datetime as dt              # 起别名 as，名字太长时省事

    print(f"math.sqrt(16) = {math.sqrt(16)}")
    print(f"pi = {pi}")
    print(f"dt.datetime.now() = {dt.datetime.now()}")

    # --- 2. __name__：判断"我是被直接运行，还是被别人 import 了" ---
    print(f"\n当前文件的 __name__ = {__name__}")
    print("直接运行本文件时 __name__ 是 '__main__'；")
    print("如果本文件被别的文件 import，__name__ 就是模块名 'learn_python'。")
    print("所以 if __name__ == '__main__': 是标准的程序入口写法。")

    # --- 3. 包（package）长什么样：就是一个带 __init__.py 的文件夹 ---
    print("""
包用来组织多文件项目，目录结构长这样:

  my_project/
  ├── main.py                # 入口文件
  └── utils/                 # 这个文件夹就是一个"包"
      ├── __init__.py        # 有这个文件，Python 才认它是包（内容可以为空）
      ├── math_tools.py      # 模块1
      └── file_tools.py      # 模块2

在 main.py 里这样用:
  from utils.math_tools import add        # 从包里导入某个函数
  import utils.file_tools as ft           # 导入整个模块并起别名

本周末实战的"批量文件整理工具"就可以这样拆:
  主程序只负责流程，具体功能拆到不同模块里，再用 import 组装。
""")

    # --- 4. Python 去哪里找模块：按 sys.path 里的目录顺序找 ---
    print("sys.path 里前两个搜索目录:")
    print(f"  1. {sys.path[0]}   <- 当前文件所在目录，排第一")
    print(f"  2. {sys.path[1]}")


# ============================================================
# 三、requests 初体验：调用真实的 HTTP API
# ============================================================

def demo_requests():
    print("\n" + "=" * 50)
    print("三、requests 调用 HTTP API")
    print("=" * 50)

    # requests 是第三方库，先检查装没装
    try:
        import requests
    except ImportError:
        print("requests 未安装，在终端运行: pip install requests")
        return

    print(f"requests 版本: {requests.__version__}")

    # 用 Open-Meteo 天气 API 演示：免费、不需要注册 API key
    url = "https://api.open-meteo.com/v1/forecast"
    params = {                         # URL 参数，requests 会自动拼到网址 ? 后面
        "latitude": 39.9,              # 纬度（北京）
        "longitude": 116.4,            # 经度（北京）
        "current_weather": "true",     # 只要当前天气
    }

    try:
        # timeout=10：10 秒没响应就抛异常，防止程序一直傻等
        resp = requests.get(url, params=params, timeout=10)
        print(f"状态码: {resp.status_code}")        # 200 表示成功
        print(f"实际请求的完整地址: {resp.url}")
        if resp.status_code == 200:
            data = resp.json()         # 返回的是 JSON，直接解析成字典
            weather = data["current_weather"]
            print(f"北京当前温度: {weather['temperature']}°C, "
                  f"风速: {weather['windspeed']} km/h")
        else:
            print(f"请求失败，状态码 {resp.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时了，检查一下网络")
    except requests.exceptions.RequestException as e:
        # RequestException 是 requests 所有异常的父类，一网打尽
        print(f"请求出异常了（可能没联网）: {e}")

    print("""
状态码速查:
  200 成功 / 404 资源不存在 / 403 禁止访问
  429 请求太频繁 / 500 服务器内部错误
这个 API 不用 key，改 latitude/longitude 就能查别的城市。
""")


# ============================================================
# 四、JSON 处理（网络数据最常用的格式）
# ============================================================

def demo_json():
    print("\n" + "=" * 50)
    print("四、JSON 处理")
    print("=" * 50)

    # JSON 长得很像 Python 的字典/列表，是网络传输数据的标准格式
    # 记两组对应关系:
    #   dumps / loads  -> 处理"字符串"（dumps 转成串，loads 解析回来）
    #   dump  / load   -> 处理"文件"（少个 s，就是读写文件版）

    # --- 1. 字典 -> JSON 字符串：dumps ---
    info = {"name": "小明", "age": 18, "hobbies": ["建模", "Python"]}
    text = json.dumps(info, ensure_ascii=False, indent=2)
    # ensure_ascii=False：让中文正常显示，否则会变成 \uXXXX 转义
    # indent=2：带缩进输出，方便人看
    print(f"dumps 结果:\n{text}")
    print(f"dumps 之后的类型: {type(text)}")       # str 字符串

    # --- 2. JSON 字符串 -> 字典：loads ---
    json_str = '{"city": "北京", "temp": 25}'
    data = json.loads(json_str)
    print(f"\nloads 结果: {data}，类型: {type(data)}")
    print(f"取 city: {data['city']}")

    # --- 3. 写入 JSON 文件：dump ---
    path = "demo.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"\n已写入文件 {path}")

    # --- 4. 从文件读 JSON：load ---
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"读回来: {loaded}")

    # --- 5. 用完删掉演示文件 ---
    os.remove(path)
    print("演示文件已删除")


# ============================================================
# 五、类型标注（给变量和函数加"类型提示"）
# ============================================================

# 注意：类型标注只是"提示"，Python 运行时不会强制检查，
# 写错了照样能运行。它的作用是:
#   1. 让 VS Code 这类编辑器帮你检查、自动补全
#   2. 让别人（和以后的你）一眼看懂函数要什么、返回什么
#   3. 可以配合 mypy 这类工具做静态检查

def add(a: int, b: int) -> int:
    """参数 a、b 应该是 int，返回值也是 int"""
    return a + b


def greet(name: str, times: int = 1) -> str:
    """name 是字符串，times 是整数，返回字符串"""
    return f"你好, {name}! " * times


def demo_type_hints():
    print("\n" + "=" * 50)
    print("五、类型标注")
    print("=" * 50)

    # --- 1. 变量标注：变量名: 类型 = 值 ---
    age: int = 18
    price: float = 9.9
    name: str = "小明"
    is_ok: bool = True
    print(f"age={age}, price={price}, name={name}, is_ok={is_ok}")

    # --- 2. 容器标注：list[元素类型] / dict[键类型, 值类型] ---
    scores: list[int] = [90, 85, 77]
    person: dict[str, int] = {"小明": 90, "小红": 85}
    point: tuple[int, int] = (3, 5)
    print(f"scores: {scores}")
    print(f"person: {person}")
    print(f"point:  {point}")

    # --- 3. 返回值可能是某种类型或 None：用 类型 | None（Python 3.10+）---
    def find_user(user_id: int) -> str | None:
        if user_id == 1:
            return "小明"
        return None                    # 找不到就返回 None

    print(f"\nfind_user(1)  = {find_user(1)}")
    print(f"find_user(99) = {find_user(99)}")

    # --- 4. 标注不会阻止你传错类型，运行照样跑 ---
    print(f"\nadd(1, 2) = {add(1, 2)}")
    print(f"add('1', '2') = {add('1', '2')}  <- 传了字符串也没报错，因为标注不强制")
    print(f"标注的意义在于编辑器提示和代码可读性")

    print("""
常用标注语法:
  x: int = 3                 变量标注
  def f(x: int) -> str:      参数和返回值标注
  list[int]                  整数列表
  dict[str, int]             键是str、值是int的字典
  tuple[int, int]            两个整数的元组
  str | None                 要么是 str 要么是 None（3.10+ 写法）
""")


# ============================================================
# 六、logging 日志（项目里别再只用 print 调试）
# ============================================================

def demo_logging():
    print("\n" + "=" * 50)
    print("六、logging 日志")
    print("=" * 50)

    print("""
print 的问题: 项目上线后没法一个个删，也分不清哪些是调试信息。
logging 的好处:
  1. 分级别（debug/info/warning/error），想输出哪个级别就输出哪个级别
  2. 可以同时写到终端和日志文件
  3. 自动带时间戳，方便排查问题
""")

    log_file = "demo.log"

    # basicConfig：一次性配置日志的级别、格式、输出位置
    # level=logging.DEBUG：DEBUG 及以上级别全都记录（最宽松）
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        # asctime=时间, levelname=级别名, message=你写的内容
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),  # 写进文件
            logging.StreamHandler(),                          # 同时打印到终端
        ],
        force=True,                    # 覆盖之前的配置（重复运行脚本时有用）
    )

    # 5 个级别从低到高: DEBUG < INFO < WARNING < ERROR < CRITICAL
    logging.debug("debug: 细节信息，调试时才看")
    logging.info("info: 一切正常，比如程序启动了")
    logging.warning("warning: 警告，有点不对劲但还能跑")
    logging.error("error: 出错了，某个功能跑不了")
    logging.critical("critical: 致命错误，程序要崩了")

    # 实用技巧：在 except 里用 logging.exception()，会自动把错误堆栈记下来
    try:
        1 / 0
    except ZeroDivisionError:
        logging.exception("除法的时候出异常了")

    print(f"\n日志同时写进了 {log_file}，文件内容如下:")
    with open(log_file, "r", encoding="utf-8") as f:
        print(f.read())

    # 收尾：关掉并移除 handler，避免残留的文件句柄影响后面的演示
    for h in logging.root.handlers[:]:
        h.close()
        logging.root.removeHandler(h)
    os.remove(log_file)
    print("演示日志文件已删除")


# ============================================================
# 七、.env 文件管理密钥（API key、密码别写死在代码里）
# ============================================================

def demo_env():
    print("\n" + "=" * 50)
    print("七、.env 密钥管理")
    print("=" * 50)

    print("""
为什么: API key、数据库密码写进代码，代码一 push 到 GitHub 就泄露了。
做法: 密钥放在 .env 文件里，代码通过"环境变量"读取；
      然后在 .gitignore 里写一行 .env，git 就不会上传它。
""")

    env_path = ".env"

    # --- 1. 先造一个演示用的 .env 文件（真实项目里是你手动创建的）---
    # 格式就是 一行一个 键=值，没有引号、没有空格
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("API_KEY=abc123secret\n")
        f.write("DB_PASSWORD=pass456\n")
    print("已生成演示用的 .env 文件")

    # --- 2. 把 .env 的内容加载进环境变量 ---
    # 标准做法是用 python-dotenv 库（终端: pip install python-dotenv）
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)          # 读取 .env，塞进 os.environ
        print("用 python-dotenv 加载成功")
    except ImportError:
        print("python-dotenv 未安装，用手动解析代替（效果一样）")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)   # 按第一个 = 拆成键和值
                    os.environ[k] = v

    # --- 3. 读取环境变量：os.environ.get(键, 默认值) ---
    # os.environ 是一个字典，装着当前所有的环境变量
    # 用 get 而不是 ["键"]：查不到时 get 返回默认值，不会报错
    api_key = os.environ.get("API_KEY", "未设置")
    db_pwd = os.environ.get("DB_PASSWORD", "未设置")
    missing = os.environ.get("NOT_EXIST", "这是默认值")
    print(f"API_KEY     = {api_key}")
    print(f"DB_PASSWORD = {db_pwd}")
    print(f"NOT_EXIST   = {missing}")

    # --- 4. 收尾：删掉演示文件，清掉塞进去的环境变量 ---
    os.remove(env_path)
    os.environ.pop("API_KEY", None)
    os.environ.pop("DB_PASSWORD", None)
    print("演示 .env 已删除，环境变量已清理")

    print("""
真实项目里的完整流程:
  1. 项目根目录新建 .env，写入  API_KEY=你的真实key
  2. 新建 .gitignore 文件，写入一行  .env
  3. 代码里  os.environ.get("API_KEY")  读取
  4. 提交一份 .env.example（只写键名不写真值），告诉别人需要配哪些
""")


# ============================================================
# 八、pytest：写你的第一个测试
# ============================================================

# pytest 是 Python 最流行的测试框架。规则很简单:
#   1. 测试文件名以 test_ 开头（如 test_tools.py）
#   2. 测试函数名以 test_ 开头
#   3. 函数里用 assert 断言：表达式为 False 时，这条测试就失败
#   4. 在终端运行 pytest，它会自动找到并执行所有测试函数

def add_numbers(a, b):
    """被测的函数（业务代码）"""
    return a + b


def test_add_numbers():
    """测试函数：验证 add_numbers 算得对不对"""
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


def test_add_numbers_wrong():
    """故意写一个会失败的测试，让你看看失败长什么样"""
    # assert 后面逗号可以跟一句失败时的说明
    assert add_numbers(1, 1) == 3, "1+1 明明等于 2，怎么会是 3"


def demo_pytest():
    print("\n" + "=" * 50)
    print("八、pytest 写第一个测试")
    print("=" * 50)

    print("""
怎么用（在终端里）:
  pip install pytest          # 先装一次
  pytest                      # 运行当前目录下所有测试
  pytest test_xxx.py          # 只运行某个文件
  pytest -v                   # 显示每条测试的详细结果

本文件里有两个测试函数:
  test_add_numbers       -> 应该通过
  test_add_numbers_wrong -> 故意失败，演示失败的样子
下面不用 pytest，直接手动调用它们演示效果:
""")

    for test_func in (test_add_numbers, test_add_numbers_wrong):
        try:
            test_func()
            print(f"[通过] {test_func.__name__}")
        except AssertionError as e:
            print(f"[失败] {test_func.__name__}: {e}")

    print("""
周末实战要求: 批量文件整理工具里至少写 1 个这样的测试函数，
比如"测试整理后文件确实被移动到了对应文件夹"。
""")


# ============================================================
# 九、venv 虚拟环境（给每个项目一套独立的库）
# ============================================================

def demo_venv():
    print("\n" + "=" * 50)
    print("九、venv 虚拟环境")
    print("=" * 50)

    print("""
为什么需要:
  项目 A 要用 requests 2.x，项目 B 要用 3.x，
  全都装在全局 Python 里就会互相打架。
  虚拟环境 = 给每个项目一个独立的小 Python，各装各的库，互不影响。

命令（全在终端里敲，不是写在代码里）:

  # 1. 在项目根目录创建虚拟环境（生成一个叫 venv 的文件夹）
  python -m venv venv

  # 2. 激活（Windows）
  venv\\Scripts\\activate
  # 激活成功后，命令行开头会出现 (venv) 字样
  # Mac/Linux 则是:  source venv/bin/activate

  # 3. 激活后安装库（只会装进这个环境，不污染全局）
  pip install requests python-dotenv pytest

  # 4. 导出依赖清单（换台电脑 / 别人拿到项目，一条命令装齐）
  pip freeze > requirements.txt
  # 别人恢复环境:  pip install -r requirements.txt

  # 5. 退出虚拟环境
  deactivate

注意:
  venv 文件夹要写进 .gitignore，不要上传到 GitHub（太大了）。
  上传 requirements.txt 就够了。
""")


# ============================================================
# 十、Git 进阶：分支 branch 与合并 merge
# ============================================================

def demo_git_branch():
    print("\n" + "=" * 50)
    print("十、Git 分支与合并")
    print("=" * 50)

    print("""
分支是什么:
  相当于"平行世界"。在新分支上随便改、随便试，
  不影响 main 分支；做完了再合并回去。

常用命令（在终端里）:

  git branch dev              # 创建 dev 分支
  git branch                  # 查看所有分支（带 * 的是当前所在）
  git checkout dev            # 切换到 dev 分支（新写法: git switch dev）
  git checkout -b dev         # 创建并切换，一步到位

  # 在 dev 分支上正常开发、提交:
  git add .
  git commit -m "完成文件整理功能"

  git checkout main           # 先切回 main 分支
  git merge dev               # 把 dev 的改动合并进 main

  git branch -d dev           # 合并完了，删掉 dev 分支
  git push                    # 推送 main 到 GitHub

合并冲突（conflict）:
  两个分支改了同一个文件的同一行，merge 时 Git 不知道该留谁的，
  会在文件里标出:
      <<<<<<< HEAD
      main 分支的内容
      =======
      dev 分支的内容
      >>>>>>> dev
  你手动决定保留哪段，删掉标记，再 git add + git commit 即可。

本周实战建议:
  写"批量文件整理工具"前先  git checkout -b dev，
  在 dev 上开发，完成后合并回 main 再 push。
""")


# ============================================================
# 十一、12 道练习题
# ============================================================

EXERCISES = [
    "练习01【异常】写 safe_int(s)：把字符串转成 int，失败时返回 None",
    "练习02【异常】写 divide(a, b)：分别捕获 ZeroDivisionError 和 TypeError",
    "练习03【异常】自定义异常 PasswordTooShortError，密码少于6位时 raise",
    "练习04【模块】import random：从名单里随机抽1人，再生成1~100随机数",
    "练习05【JSON】字典转 JSON 字符串（中文正常显示），再解析回字典",
    "练习06【JSON】把学生列表存进 json 文件，再读出来逐个打印，最后删文件",
    "练习07【类型标注】给 is_even(n) 和 filter_adults(ages) 加上完整标注",
    "练习08【logging】配置 logging 把一条 info 和一条 error 写进 my.log",
    "练习09【.env】用 os.environ.get 读取 API_KEY，读不到就返回'未设置'",
    "练习10【pytest】写 is_palindrome(s) 判断回文，并写测试函数断言3种情况",
    "练习11【requests】请求 Open-Meteo 查上海天气（纬度31.2 经度121.5）",
    "练习12【综合】读 scores.json 求平均分，结果写入 result.txt，全程异常处理",
]


def show_exercises():
    print("\n" + "=" * 50)
    print("十一、12 道练习题")
    print("=" * 50)
    print("先自己动手写，写完再看下面的 practice_01 ~ practice_12 参考答案。")
    print("想运行哪个答案，就把文件最底下的对应注释取消，再运行本文件。\n")
    for q in EXERCISES:
        print(f"  {q}")


# ============================================================
# 参考答案：先自己写！写完再对照
# ============================================================

def practice_01():
    """safe_int：转换失败返回 None"""
    def safe_int(s):
        try:
            return int(s)
        except ValueError:             # "abc" 这种转不了，会抛 ValueError
            return None

    print(safe_int("123"))             # 123
    print(safe_int("abc"))             # None


def practice_02():
    """divide：分开捕获两种异常"""
    def divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("错误: 除数是 0")
        except TypeError:
            print("错误: 参数类型不对")

    print(divide(10, 2))               # 5.0
    divide(10, 0)                      # 错误: 除数是 0
    divide(10, "a")                    # 错误: 参数类型不对


def practice_03():
    """自定义异常"""
    class PasswordTooShortError(Exception):
        pass

    def check_password(pwd):
        if len(pwd) < 6:
            raise PasswordTooShortError("密码至少要 6 位")
        print("密码合格")

    try:
        check_password("123")
    except PasswordTooShortError as e:
        print(f"抓到了: {e}")


def practice_04():
    """random 模块"""
    import random
    names = ["小明", "小红", "小刚"]
    print(f"随机点名: {random.choice(names)}")    # 随机选一个
    print(f"随机数:   {random.randint(1, 100)}")  # 1~100 闭区间


def practice_05():
    """JSON 字符串互转"""
    info = {"name": "小明", "scores": [90, 85]}
    text = json.dumps(info, ensure_ascii=False)   # 字典 -> 字符串
    back = json.loads(text)                       # 字符串 -> 字典
    print(text)
    print(f"解析回来: {back}，类型 {type(back)}")


def practice_06():
    """JSON 文件读写"""
    students = [
        {"name": "小明", "score": 90},
        {"name": "小红", "score": 85},
    ]
    path = "students.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data:
        print(f"{s['name']}: {s['score']}分")
    os.remove(path)


def practice_07():
    """类型标注"""
    def is_even(n: int) -> bool:
        return n % 2 == 0

    def filter_adults(ages: list[int]) -> list[int]:
        result: list[int] = []
        for age in ages:
            if age >= 18:
                result.append(age)
        return result

    print(f"is_even(4) = {is_even(4)}")
    print(f"成年人: {filter_adults([12, 20, 17, 30])}")


def practice_08():
    """logging 写文件"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(message)s",
        filename="my.log",             # 只写进文件，不打印到终端
        encoding="utf-8",
        force=True,
    )
    logging.info("程序正常启动")
    logging.error("这里出错了")
    # 收尾：关掉 handler 再删文件
    for h in logging.root.handlers[:]:
        h.close()
        logging.root.removeHandler(h)
    with open("my.log", "r", encoding="utf-8") as f:
        print(f"my.log 内容:\n{f.read()}")
    os.remove("my.log")


def practice_09():
    """读环境变量"""
    key = os.environ.get("API_KEY", "未设置")
    print(f"API_KEY = {key}")          # 没配置过，输出"未设置"


def practice_10():
    """回文判断 + 测试函数"""
    def is_palindrome(s: str) -> bool:
        # s[::-1] 是字符串反转；和原来一样就是回文
        return s == s[::-1]

    def test_is_palindrome():
        assert is_palindrome("level")          # 是回文
        assert is_palindrome("aba")            # 是回文
        assert not is_palindrome("hello")      # 不是回文

    test_is_palindrome()               # 没抛 AssertionError 就是全通过
    print("test_is_palindrome 全部通过")


def practice_11():
    """requests 查上海天气"""
    try:
        import requests
    except ImportError:
        print("先安装: pip install requests")
        return
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": 31.2, "longitude": 121.5,
                    "current_weather": "true"},
            timeout=10,
        )
        weather = resp.json()["current_weather"]
        print(f"上海当前温度: {weather['temperature']}°C")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


def practice_12():
    """综合：JSON 读入 -> 处理 -> 写出，全程异常处理"""
    path_in = "scores.json"
    path_out = "result.txt"

    # 先造一份测试数据（真实场景里这个文件是本来就有的）
    with open(path_in, "w", encoding="utf-8") as f:
        json.dump([88, 92, 75, 60], f)

    try:
        with open(path_in, "r", encoding="utf-8") as f:
            scores = json.load(f)
        avg = sum(scores) / len(scores)
        with open(path_out, "w", encoding="utf-8") as f:
            f.write(f"平均分: {avg:.1f}")
        print(f"处理完成，平均分 = {avg:.1f}，已写入 {path_out}")
    except FileNotFoundError:
        print("文件不存在")
    except json.JSONDecodeError:
        print("JSON 格式不对，解析失败")
    except ZeroDivisionError:
        print("成绩列表是空的，没法求平均")
    finally:
        # 不管成功失败，都把演示文件清理掉
        for p in (path_in, path_out):
            if os.path.exists(p):
                os.remove(p)
        print("演示文件已清理")


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    # 直接运行本文件时 __name__ 就是 "__main__"
    # 别的文件 import 本文件时，下面这段不会执行
    demo_exception()
    demo_module()
    demo_requests()
    demo_json()
    demo_type_hints()
    demo_logging()
    demo_env()
    demo_pytest()
    demo_venv()
    demo_git_branch()
    show_exercises()

    # ---- 练习答案：想看哪题就把哪行开头的 # 删掉，再运行 ----
    # practice_01()
    # practice_02()
    # practice_03()
    # practice_04()
    # practice_05()
    # practice_06()
    # practice_07()
    # practice_08()
    # practice_09()
    # practice_10()
    # practice_11()
    # practice_12()

    print("\n第二周演示完毕! 哪一行不懂就问我哪一行。")
