"""
测试数据加载器 — 从 Date/*.yaml 读取测试数据。

用法：
    from Common.loader import load_regions, load_users

    regions = load_regions()
    region_id = regions["regions"]["henan_zhengzhou_jinshui"]["id"]

    users = load_users()
    user_id = users["users"]["normal_user"]["id"]
"""
import os
import yaml

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Date")


def _load(filename: str) -> dict:
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_regions() -> dict:
    """返回 regions.yaml 全部内容"""
    return _load("regions.yaml")


def load_users() -> dict:
    """返回 users.yaml 全部内容"""
    return _load("users.yaml")

def load_dept() -> dict:
    """返回 dept.yaml 全部内容"""
    return _load("dept.yaml")
def load_menu() ->dict:
    return _load("menu.yaml")
def load_page() ->dict:
    return _load("page.yaml")
def load_station() ->dict:
    return _load("station.yaml")