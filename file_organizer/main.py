import logging
from pathlib import Path
from rules import get_sort
from organizer import FileOrganizer, DEFAULT_RULES
SOURCE_DIR = "test_downloads"
DRY_RUN = True
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler("organize.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("程序开始")
    rules = get_sort()
    if not rules:
        logger.warning("rules.json 读取失败，改用内置默认规则")
        rules = DEFAULT_RULES
    source = Path(SOURCE_DIR)
    if not source.is_dir():
        logger.error(f"源文件夹不存在：{source.resolve()}，请先创建")
        raise SystemExit(1)
    organizer = FileOrganizer(str(source), rules, DRY_RUN)
    organizer.organize()
    organizer.print_summary()
    logger.info("程序结束")
