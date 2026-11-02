def input_int(prompt):
    while True:
        age = input(f"{prompt}")
        try:
            return int(age)
        except ValueError: 
            print("输入无效,请重新输入")
def safe_divide():
    num1 = input("请输入被除数:")
    num2 = input("请输入除数:")
    num3 = 0
    try:
        num3 = int(num1)/int(num2)
        return num3
    except ValueError:
        print("输入无效,请输入数字")
        print("本次计算结束")
    except ZeroDivisionError:
        print("除数不能为0") 
        print("本次计算结束")
def read_scores(path):
    exam_scores = {}
    try:
        with open(path,"r",encoding="utf-8") as f:
            for line in f:
                name, score = line.split(":")
                try:
                    exam_scores[name] = int(score)
                except ValueError:
                    print(f"跳过无效行:{line}")
    except FileNotFoundError:
        print(f"文件{path}不存在")
    return exam_scores
age = input_int("请输入你的年龄: ")
print(f"你的年龄是 {age}")
num = safe_divide()
print(f"计算结果为{num}")
scores = read_scores("exam_scores.txt")
print(scores)

missing = read_scores("missing.txt")
print(missing)
