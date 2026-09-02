# ============================================================
# Python 学习示例：文件读写、函数、类、pip install
# 直接运行这个文件：python study_python.py
# 有不明白的某一行，随时问我！
# ============================================================

import json
import os


# ============================================================
# 第一部分：文件读写
# ============================================================

def demo_file_read_write():
    """演示如何读写文本文件"""
    filename = "demo_data.txt"

    # --- 写文件 ---
    # open(文件名, 模式)  mode="w" 表示写入（会覆盖旧内容）
    # with 会自动关闭文件，即使出错也不会漏关
    with open(filename, "w", encoding="utf-8") as f:
        f.write("第一行：Hello\n")
        f.write("第二行：Python\n")
        f.writelines(["第三行：学习文件\n", "第四行：读写操作\n"])

    print(f"已写入文件：{filename}")

    # --- 读整个文件 ---
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()          # 一次性读全部，得到字符串
    print("\n【read() 读全部】")
    print(content)

    # --- 按行读取 ---
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()       # 得到列表，每行一个元素（含 \n）
    print("【readlines() 按行读】")
    for i, line in enumerate(lines, start=1):
        print(f"  第{i}行: {line.rstrip()}")   # rstrip() 去掉行尾换行符

    # --- 追加内容 ---
    # mode="a" 表示 append，在文件末尾追加，不覆盖
    with open(filename, "a", encoding="utf-8") as f:
        f.write("第五行：追加的内容\n")

    print("\n【追加后】")
    with open(filename, "r", encoding="utf-8") as f:
        print(f.read())

    # --- 读写 JSON（很常用）---
    json_file = "demo_data.json"
    user = {"name": "小明", "age": 18, "skills": ["Python", "文件操作"]}

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False, indent=2)

    with open(json_file, "r", encoding="utf-8") as f:
        loaded_user = json.load(f)

    print(f"\n【JSON 读写】读取到: {loaded_user}")
    print(f"  姓名: {loaded_user['name']}")

    # 清理演示文件（可选）
    os.remove(filename)
    os.remove(json_file)
    print("\n演示文件已清理")


# ============================================================
# 第二部分：函数
# ============================================================

def greet(name, times=1):
    """
    带参数和默认值的函数

    参数:
        name  - 名字（必填）
        times - 打印次数（可选，默认 1）
    """
    for _ in range(times):
        print(f"  你好，{name}！")


def add(a, b):
    """简单函数：两数相加，用 return 返回结果"""
    return a + b


def calculate_stats(numbers):
    """
    函数可以返回多个值（实际是返回一个元组）
    """
    if not numbers:
        return 0, 0, 0

    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return total, count, average


def demo_functions():
    print("\n" + "=" * 50)
    print("第二部分：函数")
    print("=" * 50)

    greet("张三")
    greet("李四", times=3)

    result = add(10, 20)
    print(f"\nadd(10, 20) = {result}")

    nums = [3, 6, 2, 8, 4, 10]
    total, count, avg = calculate_stats(nums)
    print(f"\ncalculate_stats({nums})")
    print(f"  总和: {total}, 个数: {count}, 平均: {avg:.1f}")


# ============================================================
# 第三部分：类（面向对象）
# ============================================================

class Student:
    """
    类 = 蓝图/模板，用来创建对象
    对象 = 根据类创建的具体实例
    """

    # 类变量：所有实例共享
    school = "Python 学习学校"

    def __init__(self, name, age):
        """
        构造方法：创建对象时自动调用
        self 代表"当前这个对象本身"
        """
        self.name = name          # 实例变量：每个对象各自拥有
        self.age = age
        self.scores = []          # 初始化为空列表

    def add_score(self, subject, score):
        """实例方法：第一个参数必须是 self"""
        self.scores.append({"subject": subject, "score": score})

    def average_score(self):
        """计算平均分"""
        if not self.scores:
            return 0
        return sum(s["score"] for s in self.scores) / len(self.scores)

    def __str__(self):
        """定义 print(对象) 时显示的内容"""
        return f"Student(name={self.name}, age={self.age})"

    @classmethod
    def from_dict(cls, data):
        """
        类方法：用 @classmethod 装饰
        cls 代表类本身，常用于替代构造方式
        """
        return cls(data["name"], data["age"])


class GraduateStudent(Student):
    """继承：GraduateStudent 是 Student 的子类，拥有父类所有功能，并可扩展"""

    def __init__(self, name, age, advisor):
        super().__init__(name, age)   # 调用父类的 __init__
        self.advisor = advisor        # 子类新增的变量

    def __str__(self):
        return f"GraduateStudent(name={self.name}, advisor={self.advisor})"


def demo_classes():
    print("\n" + "=" * 50)
    print("第三部分：类")
    print("=" * 50)

    # 创建对象（实例化）
    s1 = Student("小明", 18)
    s1.add_score("数学", 90)
    s1.add_score("英语", 85)

    print(f"\n对象 s1: {s1}")
    print(f"  学校: {Student.school}")
    print(f"  平均分: {s1.average_score()}")

    # 用类方法创建对象
    s2 = Student.from_dict({"name": "小红", "age": 17})
    print(f"\n用 from_dict 创建: {s2}")

    # 继承示例
    gs = GraduateStudent("研究生小王", 24, "张教授")
    gs.add_score("论文", 95)
    print(f"\n子类对象: {gs}")
    print(f"  平均分: {gs.average_score()}")


# ============================================================
# 第四部分：pip install（第三方包）
# ============================================================

def demo_pip_and_packages():
    """
    pip 是 Python 的包管理器，用来安装别人写好的库。

    【在终端/命令行里使用，不是写在 Python 代码里】

    常用命令：
        pip install 包名              # 安装
        pip install 包名==1.2.3       # 安装指定版本
        pip uninstall 包名            # 卸载
        pip list                      # 查看已安装的包
        pip show 包名                 # 查看某个包的详情
        pip freeze > requirements.txt # 导出依赖列表
        pip install -r requirements.txt  # 批量安装

    示例（在终端运行）：
        pip install requests        # HTTP 请求库
        pip install pandas          # 数据分析
        pip install flask           # Web 框架

    安装完成后，在代码里 import 使用：
        import requests
        response = requests.get("https://httpbin.org/get")
        print(response.json())
    """
    print("\n" + "=" * 50)
    print("第四部分：pip install")
    print("=" * 50)

    print("""
pip 是在【终端】里用的命令，步骤如下：

  1. 打开终端（Windows: PowerShell 或 CMD）
  2. 输入: pip install requests
  3. 等待安装完成
  4. 在 Python 里 import requests 就能用了

下面演示：如果已安装 requests 就用它发请求；
如果没安装，会提示你去 pip install。
""")

    try:
        import requests

        print("requests 已安装！")
        print(f"  版本: {requests.__version__}")
        print("  用法示例:")
        print('    import requests')
        print('    resp = requests.get("https://example.com")')
        print("    print(resp.status_code)")

    except ImportError:
        print("requests 还没安装！请在终端运行：")
        print("  pip install requests")
        print("然后重新运行本文件。")


# ============================================================
# 主程序入口
# ============================================================

if __name__ == "__main__":
    # __name__ == "__main__" 表示这个文件是被直接运行的
    # 如果被别的文件 import，这段代码不会执行

    print("=" * 50)
    print("Python 学习示例开始运行")
    print("=" * 50)

    print("\n" + "=" * 50)
    print("第一部分：文件读写")
    print("=" * 50)
    demo_file_read_write()

    demo_functions()
    demo_classes()
    demo_pip_and_packages()

    print("\n" + "=" * 50)
    print("全部演示完成！有不明白的随时问我某一行。")
    print("=" * 50)
