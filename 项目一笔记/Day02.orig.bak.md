### 一、装饰器
定义:**装饰器就是一个“包装盒”，用 `@` 符号套在函数头上，能在不修改原函数代码的情况下，给函数动态添加额外功能。在 FastAPI 里，它主要用来告诉服务器：“这个函数是处理哪个接口的”**
1.在日常代码里面:
先在外面写好要新增的功能:
def add_time_and_memory(func):  # 接收一个参数，名字叫 func
    def wrapper():
        print("--- 加时间 ---")
        func()  # 这里的 func 就是你传进来的那个函数
        print("--- 加内存 ---")
    return wrapper
2.再将新写好的功能挂载到原函数上
@add_time_and_memory
def say_hello():
    print("你好呀！")
当你写 `@add_time_and_memory` 时，Python 在后台悄悄做了一件事：  
**它把 `say_hello` 这个函数本身，当作一个“包裹”，塞给了 `add_time_and_memory` 函数，并且赋值给了 `func` 这个变量。**
2.在FastAPI中:
@app.get("/health")
def health_check():
    return {"status": "ok"}
就是告诉服务器,遇到GET请求,并且路径是/health,就调用下面这个函数执行
如果没有装饰器，你就得自己写一大堆复杂的路由分发代码（判断 URL 是啥、请求方法是啥、去调哪个函数,一堆if-else语句），非常痛苦
eg:
def 接客大脑(请求):
    # 痛苦 1：你要手动解析请求是 GET 还是 POST
    if 请求.method == "GET":
        # 痛苦 2：你要手动判断 URL 是什么
        if 请求.url == "/health":
            返回结果 = health_check()
        elif 请求.url == "/ask":
            返回结果 = ask_question()
        else:
            返回结果 = "404 找不到"
    elif 请求.method == "POST":
        if 请求.url == "/upload":
            返回结果 = upload_file()
        # ... 几百个 if-else 嵌套 ...
但是当有了装饰器之后,我们就可以直接使用FastAPI中写好的路由分发方法,将它挂载在函数上就行
还有一个用法:**`@property`：把“动作”伪装成“属性”**
假设你写了一个类，里面有个方法叫 `get_full_name()`，用来把姓和名拼起来：
class Person:
    def __ init __ (self, first, last):
        self.first = first
        self.last = last

    def get_full_name(self):   # 这是一个方法
        return f"{self.first} {self.last}"

p = Person("张", "三")
print(p.get_full_name())  # 打印：张 三
注意上面，调用方法**必须带括号** `()`
加上@property:
class Person:
    def __ init __ (self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):       # 方法名变成了 full_name
        return f"{self.first} {self.last}"

p = Person("张", "三")
print(p.full_name)  # 打印：张 三 （注意：没加括号！）
优点:
1. **为了代码好看、读起来像自然语言**：`p.full_name` 比 `p.get_full_name()` 更符合人类直觉。
2. **为了安全**：你可以在 `@property` 方法里加逻辑，比如“如果用户没填名字，就返回‘匿名’”，同时不允许外面的人随便修改这个名字（相当于只读属性）。在没有加入`@xxx.setter`之前,都不可以修改,而`@xxx.setter`是带安检的修改
eg:
class Student:
    def __init__(self):
        self.__ score = 100

    @property
    def score(self):
        return self.__score

    # 这就是修改分数的“安检门”
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("分数必须是整数！") # 拦截类型错误
        if value < 0 or value > 100:
            raise ValueError("分数必须在 0-100 之间！") # 拦截范围错误
        
        self.__score = value  # 安检通过了，才真正修改

s = Student()
s.score = 85    # 正常通过安检，修改成功
s.score = -10   # 💥 直接报错：分数必须在 0-100 之间！
**`@property` 和 下划线私有变量，那是原配夫妻，必须一起用**
(当你修改笔记格式时,读到这里,先帮我简单介绍一下双下划线的作用,之后再简单解释一下原因,为什么要一起用,给出例子,以及不一起用的后果)
### 二、CORSMiddleware
**1.Middleware**
定义:它的名称叫做中间件,是**夹在服务器（uvicorn）和应用（FastAPI）中间的一个"加工厂"**
**它主要用于全局的请求预处理（如 CORS 跨域、身份认证、请求日志记录）和响应的后处理,它对全局生效**
**为什么要有中间件？没它不行吗？**
没它也行，但你会累死。
假设你项目里有 20 个接口（`/upload`, `/ask`, `/history`...）。
- **没有中间件**：你得在每一个接口的函数里，都手写一遍“检查跨域”、“验证用户登录”。写 20 遍，又累又容易漏。
- **有了中间件**：你只要在外面配置一次。请求一进来，先统一被中间件拦截处理，处理完再自动分发给后面的接口。**代码极其清爽**
**它和装饰器异曲同工**:
都可以使用前辈们写好的方法,只要改参数就行
就有一个疑问:为什么要检查每一个接口,不检查不行吗?
原因:
1. **防黑客**：防止跨站脚本攻击（CSRF）、恶意刷接口、爬虫。
2. **防小人**：防止没买会员的人，偷偷调用你付费的高级功能。
3. **防瞎搞**：防止前端给你传了一堆垃圾数据（比如把上传文件写成了 10 个 G），把你的服务器撑爆。
**CORSMiddleware**:
就是为了解决浏览器的**同源策略**:
**协议（http/https）、域名（IP/网址）、端口号（如 3000/8000）**。  
**只有这三样完全一模一样，浏览器才认为它们是同源。**
只要有一个不一样，就是**跨域（跨源）**
**只要不是同源，默认不准随便发请求**
目的是:保护你的Cookie、登录状态不被偷走
所以**CORSMiddleware**就是用来解决这个问题的:就是前人写了一套叫**CORS的跨域规则**,之后把它**挂载到中间件**上面去,我们只要**改一改参数**就可以用了,这也说明也还有**其他规则**可以挂载到中间件上面去
生活化例子理解:
### 🎬 第一幕：前端出门，保安拦截（浏览器层面）

1. 前端写好代码：`fetch("http://localhost:8000/ask")`。
    
2. 浏览器（保安）一看：出发地是 `3000`，目的地是 `8000`，**跨域了！**
    
3. 出于安全考虑，浏览器**不直接发送真正的业务请求**。它先自动帮你发一个**“预检请求（OPTIONS）”**，相当于问一句：“嘿，8000 端口，我是 3000 端口，我能过来吗？”
    

---

### 🎬 第二幕：请求进门，中间件查规矩（后端层面）

1. 这个“预检请求”经过 uvicorn，到达了你的 FastAPI 应用。
    
2. 注意！它**没有**直接去 `/ask` 的函数，而是**先撞上了 `CORSMiddleware`**。
    
3. 中间件拿出你给的参数（`allow_origins=["*"]`）看了看，说：“老板说了，所有端口都能进。”
    
4. 中间件**直接给浏览器回了一封信**：“可以，你让他来吧。”（这封信里带着 `Access-Control-Allow-Origin: *` 等通行证）。
    

> **注意：** 预检请求到这里就结束了，中间件直接把它挡下并回复了，**业务代码（`/ask` 函数）根本没被触发**。

---

### 🎬 第三幕：正式出击，再次过安检

1. 浏览器保安收到了中间件的回信，确认安全，于是**真正地**把业务请求（POST /ask）发了出来。
    
2. 请求再次到达后端，**又一次经过 `CORSMiddleware`**。
    
3. 中间件一看：“是正式请求，规矩符合，**放行！**”

4. 请求终于到达了 `@app.post("/ask")` 下面的业务函数。你的 RAG 逻辑开始跑，去检索、去调大模型，算出了答案。
    

---

### 🎬 第四幕：原路返回，盖章放行

1. 业务函数把答案（JSON）交回给 FastAPI。
    
2. 在把答案发回给浏览器之前，**再次经过 `CORSMiddleware`**。
    
3. 中间件做最后一步：**在返回的响应头（Header）里，强行盖上一个大红章**（`Access-Control-Allow-Origin: *`）。
    
4. uvicorn 把这个盖了章的响应发回给浏览器。
    

---

### 🎬 第五幕：保安验章，大结局

1. 浏览器保安收到了后端的响应。
    
2. 保安检查响应头，看到了中间件盖的那个“大红章”。
    
3. 保安点点头：“嗯，后端确实同意跨域了，这数据没问题。”
    
4. **放行！** 前端网页终于拿到了数据，把答案展示给用户。
### 三、include_router
include_router也是FastAPI写好的方法,作用是允许你在主程序里，把其他程序的小本子(记录路由选择的东西)“合并”过来
注意:之前说的装饰器在FastAPI中的作用是什么请求应该用什么函数执行,用来记录的就是在创建FastAPI实例时创建的一个"本子"(是自动就创建的)
拿main程序的代码来讲解:
app.include_router(v1.router, prefix="/v1", tags=["v1"])
`v1.router` 是我们自己造的一本 子登记簿 （ v1.py 第 21 行`router = APIRouter()` ,其中APIRouter()也是FastAPI的一个类）。`v1.py` 里那些`@router.post(...)` 都是往 子簿子 上登记的。
`v1.py` 里写`@router.post("/query")`中的地址是/query,如果直接将它记录到主本子里面去,就没有办法分的清其路由的选择了,所以prefix="/v1"的作用就是加上/v1前缀
`tags=["v1"]`这是**挂个招牌（给文档看的**)
所以`include_router` 干的事就是：
 把`v1.py` 那本子簿子整本抄进主簿子`app` ，并且给子簿子里所有地址统一加前缀`/v1` 。
 为什么不把所有接口直接写进`main.py` ？ 
 因为版本管理：以后要出`/v2` ，你只要再写个`v2.py` ，加一行`include_router(v2.router, prefix="/v2")` —— 老用户继续用`/v1` 不受影响,并且不用将所有接口全部写入主程序
**那 v1.py 为什么不能用 app = FastAPI()创建"本子"？**
因为这两个对象 职责不同 ：

`FastAPI()` `APIRouter()` 是什么 完整应用 （主簿） 可拆分的接口集合 （分册） 能被 uvicorn 启动吗 ✅ 能，`uvicorn app.main:app` 启动的就是它 ❌ 不能，它只是个登记簿，不是应用 能合并进别的应用吗 ❌ 不能 ✅ 能，`include_router` 就是干这个的

如果`v1.py` 里也写`app = FastAPI()` ，那你就造出了 第二个独立应用 ——它跟`main.py` 里那个`app` 完全不认识 ，`include_router` 也合并不了。最后 uvicorn 只启动其中一个，另一个白写了。