import shutil
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
def unique_path(target: Path) -> Path:
    if not target.exists():
        return target
    index = 1
    while True:
        new_target = target.parent / f"{target.stem}({index}){target.suffix}"
        if not new_target.exists():
            return new_target
        index += 1
def move_file(file: Path, target_dir: Path, dry_run: bool = True) -> Path | None:
    try:
        new_name_target = unique_path(target_dir / file.name)
        if dry_run:
            logger.info(f"[试运行] 将把 {file.name} 移到 {target_dir.name}\\{new_name_target.name}")
            return new_name_target
        target_dir.mkdir(parents=True, exist_ok=True)
        if new_name_target.name != file.name:
            logger.warning(f"发现重名：{file.name} 已存在，本次改名为 {new_name_target.name}")
        shutil.move(str(file), str(new_name_target))
        logger.info(f"移动成功：{file.name} -> {target_dir.name}\\{new_name_target.name}")
        return new_name_target
    except (PermissionError, OSError) as e:
        logger.error(f"{file.name} 移动失败：{e}")
        return None
