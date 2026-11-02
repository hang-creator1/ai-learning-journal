# 需求文档：批量文件整理工具（file_organizer）

> 第一、二周综合实战项目（覆盖全部已学知识点）
> 项目位置：`d:\python\file_organizer\`（已建 venv）
> 本文档即需求，**不需要查任何外部资料**

---

## 一、项目背景（为什么要做这个）

下载文件夹永远是重灾区：图片、文档、视频、安装包混在一起，几百个文件翻不动。
手动整理一次要十分钟，而且每周都要重来一遍——**重复劳动正是程序该干的事**。

本工具的作用：扫描一个"杂乱文件夹"，按文件类型自动分类移动到子文件夹里，全程记录日志。

整理前后对比：

```
整理前 downloads\            整理后 downloads\
├── 报告.docx                ├── documents\
├── 截图.png                 │   ├── 报告.docx
├── 电影.mp4                 │   └── 笔记.txt
├── 笔记.txt                 ├── images\
└── 安装包.exe               │   └── 截图.png
                             ├── videos\
                             │   └── 电影.mp4
                             └── others\
                                 └── 安装包.exe
```

---

## 二、核心功能（必做，6 个）

### 功能 1：扫描 + 分类规则

- 指定一个源文件夹（先写死在代码里即可，比如 `SOURCE_DIR = "test_downloads"`）
- 按**扩展名**判断文件属于哪个类别，分类规则**写在一个 JSON 配置文件里**，程序启动时读取：

```json
{
  "images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
  "documents": [".txt", ".docx", ".pdf", ".md", ".xlsx"],
  "videos":    [".mp4", ".avi", ".mkv", ".mov"],
  "music":     [".mp3", ".wav", ".flac"]
}
```

- 不在任何类别里的扩展名 → 归入 `others`
- 配置文件读取失败（文件不存在 / JSON 格式错误）→ 打印错误提示并使用一份**代码内置的默认规则**，不许崩（练 try/except + JSON）

### 功能 2：安全移动文件

- 用 `shutil.move()` 把文件移进对应的类别子文件夹
- 类别子文件夹不存在时自动创建（`os.makedirs(exist_ok=True)`）
- **重名冲突处理**：目标位置已有同名文件时，不许覆盖！自动改名为 `报告(1).docx`、`报告(2).docx` 依次递增
- 单个文件移动失败（权限不足、文件被占用等）→ 打印"xx 移动失败"，**继续处理下一个文件**，整个程序不许崩（错误隔离，和 air_quiz 一个思路）

### 功能 3：只整理"文件"，跳过子文件夹

- 扫描时遇到子文件夹直接跳过，不动它（防止把已整理好的类别文件夹又搬一遍）

### 功能 4：试运行模式（dry-run）

- 代码里设一个开关 `DRY_RUN = True`
- 为 True 时：只打印"将把 xxx 移到 images\"，**不实际移动**
- 为 False 时才真正执行 `shutil.move()`
- 作用：新脚本第一次跑一个真实文件夹前，先干跑一遍确认分类没毛病——这是保护自己的好习惯

### 功能 5：日志记录

- 用 `logging`（不许只用 print），同时输出到终端和 `organize.log` 文件
- 日志里至少包含：
  - INFO：程序开始 / 结束、每个文件移动到了哪
  - WARNING：发现重名，改名成了什么
  - ERROR：某个文件移动失败及原因

### 功能 6：汇总报告（练第一周的 f-string + 文件读写）

程序结束后做两件事：

**① 终端打印一张汇总表**（用 f-string 对齐，第一周的语法）：

```
====== 整理汇总 ======
扫描文件: 8
成功移动: 7
失败:     1
--------------------
images:    3 个
documents: 2 个
videos:    1 个
others:    1 个
```

各类别数量用一个字典统计：`{"images": 3, "documents": 2, ...}`（第一周的字典增改查）。

**② 用 `open()` 把这份汇总写进 `summary.txt`**（纯文件读写练习，和 logging 无关，自己控制内容格式）。

**③ 未识别扩展名清单**：扫描过程中把"不认识、被归进 others"的扩展名收集到一个**集合（set）**里，最后打印出来，比如：`本次未识别的扩展名: {'.exe', '.zip'}`——方便你以后决定要不要把它们加进 rules.json。

---

## 三、代码结构要求（必做）

拆成模块，别全堆在一个文件里（练"模块与包"），核心逻辑**用类组织**（练第一周的 OOP）：

```
file_organizer/
├── main.py            # 入口：创建 FileOrganizer 对象、调用它、触发汇总
├── organizer.py       # FileOrganizer 类：扫描、分类、移动、统计的主逻辑
├── rules.py           # 负责读 JSON 配置 + 提供"根据扩展名查类别"的函数
├── mover.py           # 负责移动文件、处理重名、dry-run 判断
├── rules.json         # 分类配置文件
├── test_rules.py      # pytest 测试
├── README.md          # 项目说明
├── requirements.txt   # 依赖清单
└── .gitignore         # 至少忽略 __pycache__/、venv/、organize.log、summary.txt
```

**类的骨架**（第一周第六节"类"的直接应用，照这个形状写）：

```python
class FileOrganizer:
    def __init__(self, source_dir: str, rules: dict, dry_run: bool = True):
        self.source_dir = source_dir
        self.rules = rules
        self.dry_run = dry_run
        self.stats = {"scanned": 0, "moved": 0, "failed": 0}   # 计数
        self.category_count = {}        # 各类别移动了几个
        self.unknown_exts = set()       # 未识别的扩展名（集合自动去重）

    def scan_files(self) -> list[str]:
        """返回源文件夹里所有"文件"的名字列表（跳过子文件夹）"""

    def organize(self) -> None:
        """主流程：遍历文件 -> 查类别 -> 移动 -> 更新统计"""

    def print_summary(self) -> None:
        """打印汇总表 + 写 summary.txt"""
```

- `main.py` 里必须有 `if __name__ == "__main__":` 入口，里面只做三件事：读配置 → 创建对象 → 调用方法
- 关键函数加**类型标注**，比如：

```python
def get_category(ext: str, rules: dict[str, list[str]]) -> str:
    """根据扩展名返回类别名，找不到返回 'others'"""

def unique_path(target: Path) -> Path:
    """如果 target 已存在，返回 文件名(1)、文件名(2)... 的新路径"""
```

---

## 四、知识点对照表（两周全覆盖）

写代码时对照这张表，确保每个知识点都真正用上了：

| 知识点 | 用在哪 |
|---|---|
| **week1** 变量/数据类型/f-string | 汇总表对齐输出、dry-run 提示语 |
| **week1** 条件判断与循环 | 分类判断、重名改名的 while 循环、遍历文件 |
| **week1** 列表/字典/集合 | 文件列表、rules 字典、统计字典、未识别扩展名集合 |
| **week1** 函数（参数/返回值） | rules.py、mover.py 里的各个小函数 |
| **week1** 文件读写 | open() 写 summary.txt |
| **week1** 类（OOP） | FileOrganizer 类 |
| **week1** pip | venv 里 pip freeze 出 requirements.txt |
| **week2** 异常处理 | 配置读取失败兜底、单文件移动失败隔离 |
| **week2** 模块与包 | main / organizer / rules / mover 拆分 + import |
| **week2** JSON | rules.json 配置读写 |
| **week2** 类型标注 | 所有函数签名 |
| **week2** logging | organize.log 双输出 |
| **week2** pytest | test_rules.py |
| **week2** venv | 独立环境（已建好） |
| **week2** Git 分支 | main 初始版 → dev 开发 → merge 回 main |

---

## 五、测试要求（必做，至少 1 个）

用 pytest，新建 `test_rules.py`，**至少**测这两个（测试纯函数，不需要真的移动文件）：

```python
def test_get_category_known():
    """已知扩展名要返回正确类别，如 .png -> images"""

def test_get_category_unknown():
    """没收录的扩展名要返回 others，如 .xyz"""
```

（学有余力可加：`test_unique_path`——用 pytest 的 `tmp_path` fixture 造临时文件夹测试重名改名逻辑，不会就跳过，不扣分。）

验收命令：在 `file_organizer` 目录下运行 `pytest`，全绿。

---

## 六、README.md 要求（必做）

让"陌生人拿到项目 5 分钟能跑起来"为标准，包含：

1. **项目简介**：一句话说清这是什么、解决什么问题
2. **功能列表**：上面第二部分的 6 条
3. **运行环境**：Python 版本、是否需要安装第三方库
4. **使用方法**：怎么改源文件夹、怎么开关 dry-run、怎么运行
5. **运行效果**：贴一段整理前后的目录对比 + 日志截图/文本

---

## 七、工程化要求（必做）

- [ ] 用 venv 创建独立环境（虽然本项目只用标准库，但流程要走一遍）
- [ ] `pip freeze > requirements.txt`
- [ ] Git 管理：先在 main 提交初始版本，新功能开 `dev` 分支开发，完成后 merge 回 main
- [ ] `.gitignore` 忽略 `__pycache__/`、`venv/`、`organize.log`

---

## 八、加分项（选做，核心做完再碰）

1. 支持命令行传参指定源文件夹：`python main.py D:\Downloads`（用 `sys.argv`）
2. 支持按"修改日期"分类（`2026-09` 这样的月份文件夹，用 `os.path.getmtime`）
3. 整理结束后生成 `report.json`，记录每个文件从哪移到了哪

---

## 九、自测清单（全过才算完成）

- [ ] 在 `test_downloads` 里手动造 6~8 个不同类型文件（含 2 个同名不同内容），先 `DRY_RUN=True` 跑一遍，输出符合预期
- [ ] 改 `DRY_RUN=False` 再跑，文件真实归类，同名文件自动改名无覆盖
- [ ] 把 `rules.json` 改成一个错误格式（比如删掉一个括号），程序打印错误并用默认规则继续，不崩
- [ ] 把一个文件用 WPS/记事本打开占用着再跑，该文件报"移动失败"，其余文件照常整理
- [ ] `organize.log` 里能看到完整的运行记录（含时间戳和级别）
- [ ] 终端打出汇总表，且 `summary.txt` 内容一致、扩展名集合正确
- [ ] `pytest` 全绿
- [ ] README 按第六节五条齐全

---

## 十、提交格式

```
1. 项目目录树截图/文本
2. main.py、organizer.py、rules.py、mover.py、test_rules.py 全部代码
3. README.md 内容
4. dry-run 模式的运行输出
5. 真实整理模式的运行输出 + organize.log + summary.txt 内容
6. pytest 运行结果截图
```

## 十一、评分点

| 维度 | 看什么 |
|---|---|
| 能否跑通 | 正常流程 + 自测清单的破坏场景 |
| 错误隔离 | 单文件失败不影响整体 |
| 配置化 | 规则走 JSON，不写死在代码逻辑里 |
| OOP 设计 | FileOrganizer 类的职责划分是否合理（不是把函数硬塞进类） |
| 基础语法 | f-string 表格、字典统计、集合去重是否用对了地方 |
| 模块拆分 | 入口 / 类 / 规则 / 移动职责分离，import 关系清晰 |
| 测试 | pytest 至少 2 条且断言有意义（不是 assert True） |
| 工程化 | venv、requirements.txt、git 分支记录、.gitignore |

预计代码量：120~160 行（不含 README）。
