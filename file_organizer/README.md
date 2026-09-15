# 批量文件整理工具（file_organizer）

一句话：把一个杂乱文件夹里的文件按类型（图片/文档/视频/音乐/其他）自动归类到子文件夹，全程记日志、出汇总报告。

## 功能列表

1. **扫描 + 分类**：按扩展名分类，规则写在 `rules.json`，读取失败自动用内置默认规则兜底
2. **安全移动**：`shutil.move` 归类，子文件夹自动创建，重名自动改名成 `报告(1).docx`，绝不覆盖
3. **只整理文件**：遇到子文件夹直接跳过，不会把整理好的类别文件夹又搬一遍
4. **试运行模式（dry-run）**：默认只打印"将把 xxx 移到 yyy\"，不真的动文件
5. **日志记录**：logging 同时输出到终端和 `organize.log`（INFO/WARNING/ERROR）
6. **汇总报告**：结束后打印汇总表、写 `summary.txt`、列出未识别的扩展名集合

## 运行环境

- Python 3.10+（用到了 `list[str]`、`X | None` 等新语法）
- 只用标准库；跑测试需要 pytest：`pip install pytest`

## 使用方法

1. 打开 `main.py`，改顶部两个变量：

```python
SOURCE_DIR = "test_downloads"   # 要整理的文件夹路径
DRY_RUN = True                  # 先 True 干跑确认，再改 False 来真的
```

2. 在项目目录下运行：

```powershell
python main.py
```

3. 查看结果：终端输出 + `organize.log` + `summary.txt`

## 运行效果

```
整理前 test_downloads\         整理后 test_downloads\
├── 报告.docx                  ├── documents\
├── 截图.png                   │   └── 报告.docx
├── 电影.mp4                   ├── images\
├── 笔记.txt                   │   └── 截图.png
└── 安装包.exe                 ├── videos\
                               │   └── 电影.mp4
                               └── others\
                                   └── 安装包.exe
```

dry-run 输出示例：

```
2026-09-14 20:00:00,123 INFO [mover] [试运行] 将把 截图.png 移到 images\截图.png
====== 整理汇总 ======
扫描文件: 5
成功移动: 5
失败:     0
--------------------
documents  1 个
images     1 个
...
本次未识别的扩展名: {'.exe'}
```

## 测试

```powershell
pytest
```

## 项目结构

| 文件 | 职责 |
|---|---|
| `main.py` | 入口：读配置 → 创建 FileOrganizer → 调用方法 |
| `organizer.py` | FileOrganizer 类 + 默认规则 + get_category |
| `rules.py` | 读取 rules.json 配置 |
| `mover.py` | 移动文件、重名改名、dry-run 判断 |
| `rules.json` | 分类配置（可自行增改扩展名） |
| `test_rules.py` | pytest 测试 |
