def greet(name):
    print(f"你好, {name}!")
greet("小明")
greet("小红")
greet("小刚")
def multiply(a,b=2):
    return a * b
print(multiply(5))       # 不传 b，用默认值
print(multiply(5, 3))   # 自己传 b
print(multiply(5, 0))    # 传 0
def stats(nums):
    return min(nums),max(nums),sum(nums)/len(nums)
lo, hi, avg = stats([3,1,4,1,5,9])
print(f"最小={lo}, 最大={hi}, 平均={avg:.2f}")
def grade_report(scores,pass_line=60):
    pass_count = 0
    fail_count = 0
    for key,value in scores.items():
        if(value > pass_line):
            pass_count += 1
        else:
            fail_count += 1
    return (pass_count, fail_count)
def print_report(scores, pass_line=60):
    total = grade_report(scores, pass_line)
    x, y = total
    for key,value in scores.items():
        if(value > pass_line):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}(不及格)")
    print(f"本次共{x}人及格,{y}人不及格")
data = {"小明": 85, "小红": 58, "小刚": 92, "小亮": 45}
print_report(data)
print("---")
print_report(data, pass_line=70)   # 及格线提到 70

    

