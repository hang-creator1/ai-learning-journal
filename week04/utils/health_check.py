import os
import sys
import json
from pathlib import Path
from typing import Any


def check_env_var(var_name: str) -> bool:
    """
    检查指定的环境变量是否存在。

    注意：只返回 True/False，绝不打印环境变量的值（防止泄露密码、密钥等敏感信息）。

    参数:
        var_name: 环境变量名称，如 "PATH"、"HOME"

    返回:
        True 表示存在，False 表示不存在
    """
    return var_name in os.environ


def check_json_config(file_path: str, required_keys: list[str]) -> bool:
    """
    读取 JSON 配置文件，并校验必需的字段是否齐全。

    参数:
        file_path: JSON 文件的路径
        required_keys: 必须存在的字段名列表

    返回:
        True 表示文件存在、格式正确、且所有必需字段齐全
        False 表示文件不存在、格式错误、或缺少字段
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
    except FileNotFoundError:
        print(f"[错误] 配置文件不存在: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"[错误] 配置文件格式错误（不是合法 JSON）: {file_path}")
        return False
    except Exception as e:
        print(f"[错误] 读取配置时发生未知异常: {e}")
        return False

    missing = [key for key in required_keys if key not in data]
    if missing:
        print(f"[错误] 配置文件缺少字段: {missing}")
        return False

    return True


def check_directory_writable(dir_path: str) -> bool:
    """
    检查目标目录是否存在且可写。

    参数:
        dir_path: 目录路径

    返回:
        True 表示目录存在且可写，False 表示不存在或不可写
    """
    path = Path(dir_path)

    if not path.exists() or not path.is_dir():
        return False

    return os.access(dir_path, os.W_OK)


def print_environment_info() -> None:
    """
    打印当前 Python 解释器路径与关键依赖版本。
    这个函数不返回任何东西，只负责打印信息。
    """
    print(f"[信息] Python 解释器路径: {sys.executable}")
    print(f"[信息] Python 版本: {sys.version.split()[0]}")

    # 尝试打印几个常用依赖的版本，没有安装就提示跳过
    dependencies = ["requests", "flask", "numpy", "pandas"]
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, "__version__", "未知版本")
            print(f"[信息] {dep} 版本: {version}")
        except ImportError:
            print(f"[跳过] 未安装 {dep}")


# 只有直接运行这个文件时，下面的代码才会执行
# 如果别人 import 这个模块，下面的代码不会自动运行
if __name__ == "__main__":
    print("=" * 40)
    print("环境健康检查")
    print("=" * 40)

    print(f"\n① 环境变量 PATH 存在: {check_env_var('PATH')}")
    print(f"   环境变量 FAKE_VAR 存在: {check_env_var('FAKE_VAR')}")

    print(f"\n② JSON 配置检查:")
    check_json_config("config.json", ["api_key", "model"])

    print(f"\n③ 当前目录可写: {check_directory_writable('.')}")
    print(f"   不存在的目录可写: {check_directory_writable('/fake/path')}")

    print(f"\n④ 环境信息:")
    print_environment_info()