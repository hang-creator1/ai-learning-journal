import logging
from pathlib import Path
from mover import move_file
logger = logging.getLogger(__name__)
DEFAULT_RULES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "documents": [".txt", ".docx", ".pdf", ".md", ".xlsx", ".doc"],
    "videos": [".mp4", ".avi", ".mkv", ".mov"],
    "music": [".mp3", ".wav", ".flac"],
}
def get_category(ext: str, rules: dict[str, list[str]]) -> str:
    for category, exts in rules.items():
        if ext.lower() in exts:
            return category
    return "others"
class FileOrganizer:
    def __init__(self, source_dir: str, rules: dict, dry_run: bool = True):
        self.source_dir = Path(source_dir)
        self.rules = rules
        self.dry_run = dry_run
        self.stats = {"scanned": 0, "moved": 0, "failed": 0}
        self.category_count = {}
        self.unknown_exts = set()
    def scan_files(self) -> list[Path]:
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        self.stats["scanned"] = len(files)
        return files
    def organize(self) -> None:
        for file in self.scan_files():
            ext = file.suffix if file.suffix else "（无扩展名）"
            category = get_category(ext, self.rules)
            if category == "others":
                self.unknown_exts.add(ext)
            result = move_file(file, self.source_dir / category, self.dry_run)
            if result is None:
                self.stats["failed"] += 1
            else:
                self.stats["moved"] += 1
                self.category_count[category] = self.category_count.get(category, 0) + 1
    def print_summary(self) -> None:
        lines = []
        lines.append("====== 整理汇总 ======")
        lines.append(f"扫描文件: {self.stats['scanned']}")
        lines.append(f"成功移动: {self.stats['moved']}")
        lines.append(f"失败:     {self.stats['failed']}")
        lines.append("-" * 20)
        for category, num in self.category_count.items():
            lines.append(f"{category:<10} {num} 个")
        if self.unknown_exts:
            lines.append(f"本次未识别的扩展名: {self.unknown_exts}")
        summary = "\n".join(lines)
        print(summary)
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(summary + "\n")
        logger.info("汇总已写入 summary.txt")
