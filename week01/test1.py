class Asset:
    studio = "启明建模工作室"
    def __init__(self,name,fmt,polys,size_mb):
        self.name = name
        self.fmt = fmt
        self.polys = polys
        self.size_mb = size_mb
    def level(self,polys):
        if polys >= 100000:
            return "高模"
        elif polys >= 10000:
            return "中模"
        else:
            return "低模"
    def cost(self,polys,size_mb):
        storage_cost = polys * 0.0001 + size_mb * 0.5
        print(f"存储成本要{storage_cost}元")
    def __str__(self):
        return f"{self.name} | {self.fmt} | 面数:{self.polys} | {self.size_mb:.2f}MB | {self.level(self.polys)}"
c1 = Asset("铁剑","fbx",120000,8.5)
list = []
list.append(c1)
found = False
for a in list:
    if a.name =="铁剑":
        found = True
print(found)