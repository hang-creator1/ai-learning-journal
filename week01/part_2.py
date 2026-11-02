score = 70
if score >= 90 :
    print("优秀")
elif score >= 80 :
    print("良好")
elif score >= 60 :
    print("及格")
else :
    print("不及格")
age = 17
has_id = True
if age>=18 and has_id :
    print("可以进入网吧")
else :
    print("不可以进入网吧")
total = 0
for i in range(1,51) :
    total+=i
print(total)
word = "Python"
for n in word :
    print(n)
m=5
while(m>1):
    print(m)
    m=m-1
print("发射!")
nums = [3, 7, 2, 8, 4, 10, 6]

for x in nums:
    if x % 2 != 0:
        continue
    if x >= 8:
        break
    print(x)