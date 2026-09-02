# ============================================================
# Python 入门练习（完整版）
# 内容：变量与数据类型 / 条件与循环 / 列表字典元组集合 /
#       函数 / 文件读写 / 类 / pip install / 20道基础练习题
# 运行方式：在终端执行  python learn_python.py
# 每一行都可以问我，比如"第 30 行是什么意思"
# ============================================================

import os


# ============================================================
# 一、变量与数据类型（数字/字符串/布尔）+ f-string
# ============================================================

def demo_variables():
    print("=" * 50)
    print("一、变量与数据类型")
    print("=" * 50)

    # --- 变量：存数据的"盒子"，赋值即创建，不用声明类型 ---
    age = 18              # int   整数
    height = 1.75         # float 小数（浮点数）
    name = "小明"          # str   字符串（用引号包裹）
    is_student = True     # bool  布尔，只有 True / False 两个值（首字母大写）

    # type() 可以查看任意变量/数据的类型
    print(f"age 的类型:       {type(age)}")         # <class 'int'>
    print(f"height 的类型:    {type(height)}")      # <class 'float'>
    print(f"name 的类型:      {type(name)}")        # <class 'str'>
    print(f"is_student 的类型: {type(is_student)}")  # <class 'bool'>

    # --- 数字运算 ---
    print(f"\n10 + 3  = {10 + 3}")     # 加
    print(f"10 - 3  = {10 - 3}")       # 减
    print(f"10 * 3  = {10 * 3}")       # 乘
    print(f"10 / 3  = {10 / 3}")       # 除（结果一定是小数）
    print(f"10 // 3 = {10 // 3}")      # 整除（只留整数部分）
    print(f"10 % 3  = {10 % 3}")       # 取余数（10 除 3 余 1）
    print(f"2 ** 10 = {2 ** 10}")      # 幂（2 的 10 次方）

    # --- 字符串常用操作 ---
    s = "  hello Python  "
    print(f"\n原字符串:        '{s}'")
    print(f"去掉首尾空格:    '{s.strip()}'")
    print(f"转大写:          '{s.upper()}'")
    print(f"替换:            '{s.replace('Python', 'World')}'")
    print(f"长度(含空格):    {len(s)}")
    greeting = "hello"
    print(f"拼接:            {greeting + ' world'}")
    print(f"重复3遍:         {greeting * 3}")

    # --- 布尔：比较运算的结果就是布尔值 ---
    print(f"\n3 > 2  -> {3 > 2}")      # True
    print(f"3 == 2 -> {3 == 2}")       # False（== 是比较，= 是赋值，别搞混！）
    print(f"3 != 2 -> {3 != 2}")       # True

    # --- 类型转换 ---
    a = "123"                          # 这是字符串，不能直接参与加法运算
    b = int(a)                         # int() 转成整数
    print(f"\nint('123') + 1 = {b + 1}")
    print(f"str(456) 转字符串后拼接: 编号-{str(456)}")
    print(f"float('3.5') = {float('3.5')}")

    # --- f-string 格式化（重点！）---
    price = 9.5
    count = 3
    print(f"\nf-string 里可以直接放变量: {price} 元 x {count} 个")
    print(f"也可以放表达式: 总价 = {price * count} 元")
    print(f"保留两位小数: {price * count:.2f}")      # 28.50
    print(f"数字补零到3位: {7:03d}")                 # 007


# ============================================================
# 二、条件判断与循环（if / for / while）
# ============================================================

def demo_condition_loop():
    print("\n" + "=" * 50)
    print("二、条件判断与循环")
    print("=" * 50)

    # --- if / elif / else：从上往下依次判断，命中就进入，后面不再看 ---
    score = 85
    if score >= 90:
        print("\nif 判断: 优秀")
    elif score >= 80:                  # elif = 否则如果
        print("\nif 判断: 良好")
    elif score >= 60:
        print("\nif 判断: 及格")
    else:
        print("\nif 判断: 不及格")

    # --- 逻辑运算 and / or / not ---
    age = 20
    has_ticket = True
    if age >= 18 and has_ticket:       # and：两个条件都满足才是 True
        print("逻辑运算: 可以进场")
    if age < 18 or not has_ticket:     # or：满足其一即可；not：取反
        print("逻辑运算: 不能进场")      # 这里条件不成立，所以不打印

    # --- for 循环 + range() ---
    # range(5) 生成 0,1,2,3,4（从 0 开始，不包含 5）
    print("\nrange(5):        ", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()                            # 只为换行

    # range(1, 10, 2) 从 1 到 9，每次跳 2 → 1 3 5 7 9
    print("range(1, 10, 2): ", end=" ")
    for i in range(1, 10, 2):
        print(i, end=" ")
    print()

    # for 也能遍历字符串
    for ch in "abc":
        print(f"遍历字符串: {ch}")

    # --- while 循环：条件成立就一直循环，适合"不知道要循环几次"的场景 ---
    print("\nwhile 倒数:")
    n = 3
    while n > 0:
        print(f"  {n}")
        n -= 1                         # 千万别忘了改变条件，否则死循环！
    print("  发射！")

    # --- break：立刻跳出整个循环 ---
    print("\nbreak 演示: 找到第一个偶数就停")
    for i in [1, 3, 4, 5, 6]:
        if i % 2 == 0:
            print(f"  找到偶数 {i}，跳出循环")
            break
        print(f"  {i} 是奇数，继续找")

    # --- continue：跳过本轮剩下的代码，直接进入下一轮 ---
    print("continue 演示: 只打印偶数")
    for i in range(6):
        if i % 2 != 0:
            continue                   # 奇数跳过不打印
        print(f"  {i}")


# ============================================================
# 三、列表 / 字典 / 元组 / 集合 —— 增删改查与遍历
# ============================================================

def demo_containers():
    print("\n" + "=" * 50)
    print("三、列表 / 字典 / 元组 / 集合")
    print("=" * 50)

    # ============ 1. 列表 list：有序、可增删改，最常用 ============
    fruits = ["苹果", "香蕉", "橘子"]
    print(f"\n列表: {fruits}")

    # 增
    fruits.append("葡萄")              # 末尾追加一个
    fruits.insert(1, "芒果")           # 在下标 1 的位置插入
    print(f"增加后: {fruits}")

    # 删
    fruits.remove("香蕉")              # 按值删除
    popped = fruits.pop()              # 删除末尾元素并返回它
    print(f"删除后: {fruits}，pop 出来的是: {popped}")

    # 改
    fruits[0] = "西瓜"                 # 按下标改（下标从 0 开始）
    print(f"修改后: {fruits}")

    # 查
    print(f"第 1 个元素: {fruits[0]}，包含西瓜吗: {'西瓜' in fruits}")
    print(f"长度: {len(fruits)}")

    # 遍历
    print("遍历: ", end=" ")
    for f in fruits:
        print(f, end=" ")
    print()

    # ============ 2. 字典 dict：键值对，靠 key 找 value ============
    student = {"name": "小明", "age": 18}
    print(f"\n字典: {student}")

    # 增 / 改（key 已存在就是改，不存在就是增）
    student["score"] = 92              # 新增一个键值对
    student["age"] = 19                # 修改已有的键
    print(f"增改后: {student}")

    # 查
    print(f"name = {student['name']}")
    print(f"get 查不存在的 key 给默认值: {student.get('phone', '没登记')}")

    # 删
    student.pop("score")
    print(f"删除 score 后: {student}")

    # 遍历：items() 同时拿到键和值
    for key, value in student.items():
        print(f"  {key}: {value}")
    print(student.get("city"))

    # ============ 3. 元组 tuple：像列表，但创建后不能改 ============
    point = (3, 5)
    x, y = point                       # 解包：一次拆给两个变量
    print(f"\n元组: {point}，解包后 x={x}, y={y}")
    # point[0] = 9                     # 取消注释试试，会报 TypeError（元组不可修改）

    # ============ 4. 集合 set：自动去重、无序 ============
    nums = [1, 2, 2, 3, 3, 3]
    unique = set(nums)                 # 列表转集合，重复的自动消失
    print(f"\n列表 {nums} 去重后: {unique}")

    a = {1, 2, 3}
    b = {2, 3, 4}
    print(f"交集（都有的）:   {a & b}")
    print(f"并集（合起来的）: {a | b}")
    print(f"差集（a有b没有）: {a - b}")


# ============================================================
# 四、函数（参数 / 返回值 / 作用域）
# ============================================================

def say_hi(name):
    """最简单的函数：接收一个参数，没有返回值"""
    print(f"你好, {name}!")


def power(base, exp=2):
    """带默认参数的函数：exp 不传时默认是 2"""
    return base ** exp


def min_max(numbers):
    """一次返回两个值（其实返回的是一个元组，接收时自动拆开）"""
    return min(numbers), max(numbers)


message = "我是全局变量"                # 全局变量：写在所有函数外面，谁都能读


def demo_functions():
    print("\n" + "=" * 50)
    print("四、函数")
    print("=" * 50)

    say_hi("张三")

    print(f"power(3)      = {power(3)}")       # 用默认 exp=2
    print(f"power(3, 3)   = {power(3, 3)}")    # 自己传 exp=3

    lo, hi = min_max([7, 2, 9, 4])
    print(f"min_max 结果  = 最小 {lo}, 最大 {hi}")

    # --- 作用域：一个变量能在多大范围里被访问 ---
    print("\n--- 作用域 ---")
    x = 10                             # 局部变量：只在本函数内有效

    def inner():                       # 函数里还可以定义函数
        x = 20                         # 这是 inner 自己的 x，不影响外面的 x
        print(f"inner 里面的 x = {x}")

    inner()
    print(f"inner 外面的 x = {x}  <- 没被 inner 改掉")
    print(f"函数里可以读全局变量: {message}")


# ============================================================
# 五、文件读写
# ============================================================

def demo_file():
    print("\n" + "=" * 50)
    print("五、文件读写")
    print("=" * 50)

    path = "note.txt"

    # --- 1. 写文件（"w" 模式：文件不存在就新建，存在就清空重写）---
    with open(path, "w", encoding="utf-8") as f:
        f.write("今天学了函数\n")
        f.write("今天学了文件读写\n")
    print("写入完成")

    # --- 2. 逐行读文件（最常用）---
    print("逐行读取:")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            print(f"  {line.strip()}")          # strip() 去掉行首尾的空白和换行

    # --- 3. 追加（"a" 模式：在文件末尾接着写，不动原内容）---
    with open(path, "a", encoding="utf-8") as f:
        f.write("这是追加的一行\n")
    print("追加完成")

    # --- 4. 一次性读出所有内容 ---
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"文件完整内容:\n{text}")

    # --- 5. 用完删掉演示文件 ---
    os.remove(path)
    print("演示文件已删除")


# ============================================================
# 六、类（面向对象）
# ============================================================

class BankAccount:
    """一个银行账户类：演示属性和方法"""

    bank_name = "Python 银行"          # 类属性：所有账户共享

    def __init__(self, owner, balance=0):
        # __init__ 在创建对象时自动执行
        # self 指代"当前这个对象"
        self.owner = owner              # 实例属性：每个账户各自一份
        self.balance = balance

    def deposit(self, amount):
        """存款"""
        self.balance += amount

    def withdraw(self, amount):
        """取款：余额不够就拒绝"""
        if amount > self.balance:
            print(f"{self.owner} 余额不足, 取款失败")
            return False
        self.balance -= amount
        return True

    def __str__(self):
        # print(对象) 时会自动调用这个方法
        return f"{BankAccount.bank_name} | 户主: {self.owner} | 余额: {self.balance} 元"


class SavingsAccount(BankAccount):
    """继承：储蓄账户, 拥有 BankAccount 的全部功能, 再加利息"""

    def add_interest(self, rate):
        """按利率给余额计息"""
        interest = int(self.balance * rate)
        self.balance += interest
        print(f"{self.owner} 收到利息 {interest} 元")


def demo_class():
    print("\n" + "=" * 50)
    print("六、类")
    print("=" * 50)

    acc = BankAccount("小明", 100)
    acc.deposit(50)
    acc.withdraw(30)
    print(acc)                          # 触发 __str__

    acc.withdraw(9999)                  # 余额不够, 会失败

    saving = SavingsAccount("小红", 1000)
    saving.add_interest(0.03)
    print(saving)                       # 储蓄账户也能用父类的方法和 __str__


# ============================================================
# 七、pip install
# ============================================================

def demo_pip():
    print("\n" + "=" * 50)
    print("七、pip install")
    print("=" * 50)

    print("""
pip 是在终端里用的命令(不是写在 .py 代码里):

  安装包:        pip install requests
  安装指定版本:  pip install requests==2.31.0
  卸载:          pip uninstall requests
  查看装了哪些:  pip list
  换国内源加速:  pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

安装好之后, 在代码里 import 就能用了。
下面演示检测一个第三方库装没装:
""")

    try:
        import requests
        print(f"requests 已安装, 版本 {requests.__version__}")
    except ImportError:
        print("requests 未安装, 在终端运行: pip install requests")


# ============================================================
# 八、20 道基础练习题
# ============================================================

EXERCISES = [
    "练习01【变量+f-string】定义 name='小明'、age=18，打印：小明今年18岁",
    "练习02【数字运算】长 5 宽 3 的矩形，打印面积和周长",
    "练习03【类型转换】把字符串 '123' 转成数字，加 1 后打印",
    "练习04【f-string格式】把 3.14159 保留两位小数打印（输出 3.14）",
    "练习05【if】n=7，判断打印 奇数 还是 偶数（提示: n % 2）",
    "练习06【if-elif-else】score=85：>=90优秀 / >=80良好 / >=60及格 / 否则不及格",
    "练习07【逻辑运算】n=21，判断它能否同时被 3 和 7 整除",
    "练习08【for】求 1+2+3+...+100 的和",
    "练习09【嵌套for】打印九九乘法表",
    "练习10【while】从 10 倒数到 1，每个数一行",
    "练习11【while】1+2+3+... 加到第几个数时，总和首次超过 100？",
    "练习12【列表】不用 max()，求 [3,1,4,1,5,9,2,6] 的最大值",
    "练习13【列表】把 [1,2,3,4,5] 每个元素平方，得到新列表",
    "练习14【列表】统计 [3,7,2,8,4,10,6] 中偶数有几个",
    "练习15【元组】p=(3,5)，解包给 x、y 并打印",
    "练习16【集合】把 [1,2,2,3,3,3] 去重后打印",
    "练习17【字典】{'小明':90,'小红':85,'小刚':58}，遍历打印每人成绩，低于60标记不及格",
    "练习18【字典】用 get() 查 '小亮' 的成绩，查不到返回默认值 0",
    "练习19【函数】写 greet(name, times=1)，打印 times 次 '你好, xxx'",
    "练习20【函数】写 min_and_max(numbers) 同时返回最小值和最大值，用两个变量接住",
]


def show_exercises():
    print("\n" + "=" * 50)
    print("八、20 道基础练习题")
    print("=" * 50)
    print("先自己动手写，写完再看下面的 practice_01 ~ practice_20 参考答案。")
    print("想运行哪个答案，就把文件最底下的对应注释取消，再运行本文件。\n")
    for q in EXERCISES:
        print(f"  {q}")


# ============================================================
# 参考答案：先自己写！写完再对照
# ============================================================

def practice_01():
    """变量 + f-string"""
    name = "小明"
    age = 18
    print(f"{name}今年{age}岁")


def practice_02():
    """数字运算"""
    length, width = 5, 3
    print(f"面积 = {length * width}, 周长 = {(length + width) * 2}")


def practice_03():
    """类型转换"""
    s = "123"
    n = int(s)                          # 字符串转整数
    print(n + 1)                        # 124


def practice_04():
    """f-string 保留两位小数"""
    pi = 3.14159
    print(f"{pi:.2f}")                  # 3.14


def practice_05():
    """if 判断奇偶"""
    n = 7
    if n % 2 == 0:                      # 能被 2 整除就是偶数
        print("偶数")
    else:
        print("奇数")


def practice_06():
    """if-elif-else 成绩等级"""
    score = 85
    if score >= 90:
        print("优秀")
    elif score >= 80:
        print("良好")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")


def practice_07():
    """逻辑运算"""
    n = 21
    if n % 3 == 0 and n % 7 == 0:
        print(f"{n} 能同时被 3 和 7 整除")
    else:
        print(f"{n} 不能同时被 3 和 7 整除")


def practice_08():
    """for 求和"""
    total = 0
    for i in range(1, 101):             # 1 ~ 100
        total += i
    print(total)                        # 5050


def practice_09():
    """九九乘法表"""
    for i in range(1, 10):
        for j in range(1, i + 1):       # j 只到 i，形成三角形
            print(f"{j}x{i}={i * j}", end="\t")
        print()                         # 一行结束换行


def practice_10():
    """while 倒数"""
    n = 10
    while n >= 1:
        print(n)
        n -= 1


def practice_11():
    """while 累加超过 100"""
    total = 0
    i = 1
    while total <= 100:
        total += i
        i += 1
    print(f"加到 {i - 1} 时，总和 {total} 首次超过 100")


def practice_12():
    """不用 max() 求最大值"""
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    biggest = nums[0]                   # 先假设第一个最大
    for n in nums:
        if n > biggest:                 # 发现更大的就更新
            biggest = n
    print(biggest)                      # 9


def practice_13():
    """列表元素平方"""
    nums = [1, 2, 3, 4, 5]
    result = []
    for n in nums:
        result.append(n ** 2)
    print(result)                       # [1, 4, 9, 16, 25]


def practice_14():
    """统计偶数个数"""
    nums = [3, 7, 2, 8, 4, 10, 6]
    count = 0
    for n in nums:
        if n % 2 == 0:
            count += 1
    print(count)                        # 5


def practice_15():
    """元组解包"""
    p = (3, 5)
    x, y = p
    print(f"x={x}, y={y}")


def practice_16():
    """集合去重"""
    nums = [1, 2, 2, 3, 3, 3]
    print(set(nums))                    # {1, 2, 3}


def practice_17():
    """字典遍历"""
    scores = {"小明": 90, "小红": 85, "小刚": 58}
    for name, score in scores.items():
        if score < 60:
            print(f"{name}: {score}分，不及格")
        else:
            print(f"{name}: {score}分")


def practice_18():
    """字典 get 默认值"""
    scores = {"小明": 90, "小红": 85}
    print(scores.get("小亮", 0))        # 查不到，返回默认值 0


def practice_19():
    """带默认参数的函数"""
    def greet(name, times=1):
        for _ in range(times):          # _ 表示"这个循环变量我用不到"
            print(f"你好, {name}")

    greet("张三")
    greet("李四", times=3)


def practice_20():
    """函数返回多个值"""
    def min_and_max(numbers):
        return min(numbers), max(numbers)

    lo, hi = min_and_max([7, 2, 9, 4])
    print(f"最小 {lo}, 最大 {hi}")


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    # 直接运行本文件时 __name__ 就是 "__main__"
    # 别的文件 import 本文件时, 下面这段不会执行
    demo_variables()
    demo_condition_loop()
    demo_containers()
    demo_functions()
    demo_file()
    demo_class()
    demo_pip()
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
    # practice_13()
    # practice_14()
    # practice_15()
    # practice_16()
    # practice_17()
    # practice_18()
    # practice_19()
    # practice_20()

    print("\n全部演示完毕! 哪一行不懂就问我哪一行。")
