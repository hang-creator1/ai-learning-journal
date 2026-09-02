fruits = ["苹果", "香蕉", "橘子"]
fruits.append("葡萄")
fruits.insert(1,"芒果")
fruits.remove("香蕉")
fruits[0]="西瓜"
print(fruits)
scores = {"小明":92,"小红":85,"小刚":58,"小亮":76}
for key,value in scores.items():
    if(value<60):
        print(f"{key}: {value}分(不及格)")
    else:
        print(f"{key}: {value}分")
appear = {}
words = ["apple","banana","apple","cherry","banana","apple"]
for key in words:
    appear[key] = appear.get(key,0)+1
print(appear)
point = (3,5)
x,y = point
print(f"坐标: x={x}, y={y}")
a = [1, 2, 2, 3, 4, 4]
b = [3, 4, 5, 5, 6]
unique1 = set[int](a)
unique2 = set[int](b)
print(unique1 & unique2)
total = 0
prices = [10.5, 20, 15.5, 8]
for i in prices:
    total +=i
print(f"总价: {total}元")
students = [
    {"name": "小明", "score": 90},
    {"name": "小红", "score": 58},
    {"name": "小刚", "score": 85}
]
max=90
key=""
for m in students:
    for key,value in student.items():
        if(value > 90):
            max = value
            key2 = key
print(f"最高分: {key2} {max}分")