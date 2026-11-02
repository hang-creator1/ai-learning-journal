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
        return storage_cost
    def __str__(self):
        return f"{self.name} | {self.fmt} | 面数:{self.polys} | {self.size_mb:.2f}MB | {self.level(self.polys)}"
def manu(list):
    while True:
        print("""===== 3D 资产仓库 =====
1. 登记资产
2. 显示所有资产
3. 查询资产
4. 仓库统计
5. 保存并退出
请选择(1-5):""")
        try:
            num = int(input())
            if num not in range(1,6):
                print("输入无效,请输入1-5:")
            elif num == 1:
                register_asset(list)
            elif num == 2:
                display_assets(list)
            elif num ==3:
                query_name = input("请输入你要查询的资产的名字:")
                query_assets(list,query_name)
            elif num ==4:
                stats_repo(list)
            elif num ==5:
                save_exit(list)
                break
        except ValueError:
            print("输入无效,请输入1-5:")
def register_asset(list):
        name = input("请输入资产名:")
        same_name = False
        for a in list:
            if a.name ==name:
                same_name = True
        if same_name == True:
            print("该资产已存在,放弃本次登记")
            return
        fmt = input("请输入格式:")
        while True:
            polys = input("请输入面数:")
            try:
                polys = int(polys)
                if polys>0:
                    break
                else:
                    print("面数无效，请输入正整数:")
            except ValueError:
                print("面数无效，请输入正整数:")
        while True:
            size_mb = input("请输入大小:")
            try:
                size_mb = float(size_mb)
                if size_mb > 0:
                    break
                else:
                    print("大小无效 并重新输入:")
            except ValueError:
                print("大小无效 并重新输入:")
        c2 = Asset(name,fmt,polys,size_mb)
        list.append(c2)
        print("登记完成")
        return name,fmt,polys,size_mb
def display_assets(list):
    if len(list) == 0:
        print("仓库内部没有任何资产,显示所有资产结束")
        return
    for a in list:
        print(a)
    print(f"共 {len(list)} 个资产")
def query_assets(list,query_name):
    if len(list) == 0:
        print("内部没有任何资产,查询结束")
        return
    else:
        for a in list:
            if a.name ==query_name:
                print(a)
                return
        print(f"查无此资产:{query_name}")
def stats_repo(list):
    if len(list) == 0:
        print("仓库是空的,无法统计")
        return  
    count = 0
    sum_polys = 0
    for a in list:
        count += 1
        sum_polys += a.polys
    try:
        avg_polys = sum_polys / count
        print(f"该仓库的平均面数为:{avg_polys:.2f}")
    except ZeroDivisionError:
        print("该仓库里面没有任何资产")
    max = list[0].cost(list[0].polys,list[0].size_mb)
    max_name = list[0].name
    for b in list:
        if b.cost(b.polys,b.size_mb) > max:
            max = b.cost(b.polys,b.size_mb)
            max_name = b.name
    print(f"存储成本最高的资产名为:{max_name},成本为:{max:.2f}元")
    low_count = 0
    for c in list:
        if c.polys < 10000:
            low_count += 1
    print(f"低模资产: {low_count}/{count}")
def save_exit(list):
    path =  "assets.txt"
    with open(path,"w",encoding="utf-8") as f:
        for a in list:
            f.write(f"{a.name}:{a.fmt}:{a.polys}:{a.size_mb}\n")
path = "assets.txt"
list = []
alreadly_count = 0
try:
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line =="":
                continue
            parts = line.split(":")
            if len(parts) != 4:
                print(f"跳过无效行:{line}")
                continue
            try:
                parts[2] = int(parts[2])
            except ValueError:
                print(f"跳过无效行:{line}")
                continue
            try:
                parts[3] = float(parts[3])
            except ValueError:
                print(f"跳过无效行:{line}")
                continue
            c = Asset(parts[0],parts[1],parts[2],parts[3])
            list.append(c)
            alreadly_count += 1
        print(f"已加载{alreadly_count}个资产")
        manu(list)
except FileNotFoundError:
    print("首次使用,仓库为空")
    manu(list)