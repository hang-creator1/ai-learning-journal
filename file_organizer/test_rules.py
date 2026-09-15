from organizer import get_category
from mover import unique_path
RULES = {
    "images": [".jpg", ".png"],
    "documents": [".txt", ".docx"],
    "videos": [".mp4"],
    "music": [".mp3"],
}
def test_get_category_known():
    assert get_category(".png", RULES) == "images"
    assert get_category(".docx", RULES) == "documents"
    assert get_category(".mp4", RULES) == "videos"
def test_get_category_unknown():
    assert get_category(".xyz", RULES) == "others"
    assert get_category("", RULES) == "others"
def test_get_category_case_insensitive():
    assert get_category(".PNG", RULES) == "images"
def test_unique_path(tmp_path):
    target = tmp_path / "a.txt"
    assert unique_path(target) == target
    target.touch()
    assert unique_path(target).name == "a(1).txt"
    (tmp_path / "a(1).txt").touch()
    assert unique_path(target).name == "a(2).txt"
