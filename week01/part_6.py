class Pet():
    hospital = "萌宠医院"
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def eat(self,food):
        print(f"{self.name}吃了{food}")
    def __str__(self):
        return(f"{self.hospital} | {self.name} | {self.age}")
class Cat(Pet):
        def __init__(self,name,age,color):
            super().__init__(name,age)
            self.color = color
        def eat(self,food):
            print(f"{self.name}优雅地吃了{food}")
c1 = Pet("小橘",2)
c2 = Cat("小花",1,"五颜六色")
c1.eat("鱼")
c2.eat("鱼")
print(c1)
print(c2)