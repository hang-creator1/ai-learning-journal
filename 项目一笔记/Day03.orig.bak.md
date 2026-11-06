### 一、Annotated and Any
### `Any`：随便，我都要

- **字面意思**：任何类型。
    
- **大白话**：**“管你是什么牛鬼蛇神，我都收。”**（可以是整数、字符串、列表、字典、甚至是一个对象）。
    
- **比喻**：就像快递站里贴了“杂物”标签的箱子，不管你是塞进去一件衣服，还是一块砖头，快递站都不管。
当前端传来的数据非常多,每个数据的位置也不同时,**FastAPI虽然是聪明的分拣员，但如果只看到普通的 Python 类型注解（比如 `str`），它也不知道该去哪个口袋里掏**,但是后端要用这些数据,那就引出了**Annotated**
语法长这样:
名字: Annotated`[什么类型, 去哪找的指令]`
它不仅告诉FastAPI是**什么类型，还写清楚“去哪找”**
FastAPI 官方早就为你准备好了几个“指令”。你只要把它们写在Annotated里，FastAPI就知道去哪找了：
**1. `Form(...)` —— 去“表单”里找**  
如果前端是通过网页表单提交的文字数据（比如“备注”），你就用 `Form`。

**2. `File(...)` —— 去“文件”里找**  
如果前端传的是一个真实的文件（比如 PDF、图片），你就用 `File`。

**3. `Query(...)` —— 去“网址问号后面”找**  
如果前端是在浏览器地址栏里敲了 `?搜索词=珍珠奶茶`，你就用 `Query`。

**4. 不贴便利贴（默认行为）**  
如果你啥都不贴，就写个普通的 `名字: str`。  
店员会**自作主张**，默认去网址问号后面（`Query`）找。找不到就不理你。
eg:
`file: Annotated[UploadFile, File(...)]`
**翻译**：这个参数叫 `file`。它的便利贴上写着：它是 `UploadFile`（文件类型）。**去 `File`（文件区）给我把它掏出来**
有一个特殊的:
store: QdrantStore = Depends(get_store)
这个长得不一样，没有用 `Annotated`。它用的是 `Depends`。
- **翻译**：意思是“别去包裹里找了，这东西不在包裹里。你去把内部员工 `get_store` 叫过来，让他准备好，把结果直接塞给 `store`
Annotated不止还可以让FastAPI知道数据该去哪里找,还可以加上检验条件,之后让FastAPI调用Pydantic去检验前端传过来的数据符不符合要求
拿这段代码来举例:
`collection: Annotated[str, Form(...)]`
其中`. . .`: **管的是“必须有这个字段”，不管“数据类型”。数据类型是由前面的 `str` 或 `int` 来管的**
1. **`str`**：这是**数据类型**的要求。意思是前端传过来的东西，**必须是文字**（不能传数字，不能传文件）。
2. **`Form(...)` 里面的 `...`**：这是**必填项**的要求。意思是前端**必须得给我传这个字段**（不能什么都不传，不能是空值）。
但是你觉得光必填还不够，要求还得限制字数。你就可以直接把规则写在 `Form` 的括号里:
`collection: Annotated[str, Form(min_length=3, max_length=20, ...)]`
**这行代码同时干了三件事：**
3. **去哪找？** `Form` 告诉 FastAPI：“去表单里找！”（这是你刚才学懂的）。
4. **什么规矩？** `min_length=3` 告诉 Pydantic：“找出来的字，必须大于 3 个！”（这是师傅之前给你讲的“安检尺子”）。
5. **必须传？** `...` 告诉 FastAPI：“要是包裹里没有这东西，直接打回，不准给默认值！”
像min_length, max_length等等这些是FastAPI里面的Form,Query等等这些函数的参数,到时候直接用即可
### 二、Depends(依赖注入)
**依赖，就是你干活之前必须准备好的东西**
**依赖注入（Depends）就是：你需要的工具，你不需要自己去造，FastAPI 会提前帮你造好、塞进你手里**
假如没有依赖注入,会有多麻烦:
**没有依赖注入,就普通的函数调用:**
`# 这是你写的一个连接数据库的函数`
def get_db_connection():
    print("正在连接数据库...")
    return "数据库连接对象"
   `# 你的接口`
@app.post("/upload")
def upload_file():
    # 痛点 1：你必须在函数里面，**手动调用**连接函数
    db = get_db_connection()
    # 痛点 2：如果**接口报错了**，你得**手动写代码去关闭数据库**
    # 痛点 3：如果明天再加 10 个接口，你要在这 10 个接口里，把这两行代码抄 10 遍！
    
    return "上传成功"
**这种写法，代码全堆在函数里，又臭又长，稍微漏写一行，数据库连接就爆满了**
**有了依赖注入会有什么样的魔法**:
你只要在接口参数里，写上 `db = Depends(get_db_connection)`
def get_db_connection():
    print("【FastAPI后台】正在连接数据库...")
    return "数据库连接对象"
`# 你的接口`
@app.post("/upload")
def upload_file(db = Depends(get_db_connection)):
    # 注意：你根本没写 db = get_db_connection()
    # 但你拿到这个函数时，db 里面已经有值了！
    print("我在用数据库干活：", db)
    return "上传成功"
**FastAPI 在后台到底干了什么？**

1. 用户请求打到了 `/upload`。
    
2. FastAPI 看到函数参数里有 `Depends(get_db_connection)`。
    
3. **FastAPI 立刻拦住请求**，说：“老板有要求，先跑一下 `get_db_connection`。”
    
4. FastAPI 自己去调用了 `get_db_connection()`，拿到了返回值（数据库对象）。
    
5. FastAPI 把返回值塞进 `db` 这个参数里。
    
6. **FastAPI 这才真正开始执行你的 `upload_file` 函数。**
**所以说,`db` 的数据，是 FastAPI 强行“注入”给你的。你只管用，不用管怎么来**
这样先去执行依赖代码,倘若依赖代码中有错误的话,要执行的主代码也不会被执行,而如果是普通函数调用的话,你是手动调用函数,你执行到依赖代码那里发现有错误的时候,你的主函数已经被执行了

`Depends` 解决的是**大厂工程里的致命问题**：
**杀手锏 1：全局复用（不用写重复代码）**  
如果你有 50 个接口都要连数据库。

- 普通写法：你写 50 遍 `db = get_db_connection()`。
    
- Depends：你在 50 个接口的参数里都加上 `db = Depends(get_db_connection)`。以后连接逻辑改了，你只需要改 `get_db_connection` 这一个函数，其他 50 个接口全部自动生效。
    

**杀手锏 2：一键替换假数据（测试神器）**  
你写测试的时候，不想每次都去连真的 Qdrant 数据库（太慢了）。  
如果你在代码里写死了 `db = get_db_connection()`，测试时必须连真库。  
如果你用了 `Depends`，FastAPI 允许你在测试时，**瞬间把 `get_db_connection` 替换成一个返回“假数据”的函数**。业务代码一行都不用改，测试速度起飞。
Depends如何让测试的时候"偷懒"
假设你项目里有这么一段代码（**注意：这是生产环境代码，绝对不能动**）：
`# 1. 真实的连接数据库函数`
def get_real_db():
    return "🔥 连上了真实的 Qdrant 数据库"

`# 2. 你的业务接口`
@app.get("/ask")
def ask_question(db = Depends(get_real_db)):
    return {"msg": "查询成功", "db_info": db}
现在你要写测试了，你不想连真数据库，你想换成一个假数据库。
**你怎么做？你不需要改上面那段代码的一个标点符号。**  
你只需要在**测试文件**（比如 `test_api.py`）里，写这几行代码：
from fastapi.testclient import TestClient
from main import app, get_real_db     # 把主程序和真函数导进来
`# 1. 写一个假函数
def get_fake_db():
    return "🧪 这是一个假的内存数据库"
`# 2. 🪄 魔法降临：告诉 FastAPI，遇到 get_real_db，统统换成 get_fake_db！`
`app.dependency_overrides[get_real_db] = get_fake_db`

`# 3. 开始测试`
client = TestClient(app)
response = client.get("/ask")

`# 4. 你会看到，返回的结果里，用的是假数据库！`
print(response.json()) 
`# 输出：{"msg": "查询成功", "db_info": "🧪 这是一个假的内存数据库"}`
其中**`TestClient` 是 FastAPI 官方提供的测试工具，它是一个类,底层基于 `httpx`。它不需要启动真实的 `uvicorn` 服务器，它可以**模拟**一个真实的用户,能直接模拟浏览器向你的 FastAPI 应用发送请求，用于编写极速、免网络的接口单元测试。**