import os
import yaml

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Date")


def _load(filename: str) -> dict:
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _auto_load(name: str) -> dict:
    return _load(f"{name}.yaml")


# === 原有 (backward compatible) ===
def load_regions():
    return _load("regions.yaml")

def load_users():
    return _load("users.yaml")

def load_dept():
    return _load("dept.yaml")

def load_menu():
    return _load("menu.yaml")

def load_page():
    return _load("page.yaml")

def load_station():
    return _load("station.yaml")


# === 共享数据 ===
def load_common():
    return _load("common.yaml")


# === System 模块 ===
def load_system_role():
    return _load("system_role.yaml")

def load_system_user():
    return _load("system_user.yaml")

def load_system_dict():
    return _load("system_dict.yaml")

def load_system_post():
    return _load("system_post.yaml")

def load_system_company():
    return _load("system_company.yaml")

def load_system_banner():
    return _load("system_banner.yaml")

def load_system_notice():
    return _load("system_notice.yaml")

def load_system_area():
    return _load("system_area.yaml")

def load_system_auth():
    return _load("system_auth.yaml")

def load_system_oauth2():
    return _load("system_oauth2.yaml")

def load_system_tenant():
    return _load("system_tenant.yaml")


# === Recycle 模块 ===
def load_recycle_station_express():
    return _load("recycle_station_express.yaml")

def load_recycle_admin_order():
    return _load("recycle_admin_order.yaml")

def load_recycle_activity():
    return _load("recycle_activity.yaml")

def load_recycle_clear_order():
    return _load("recycle_clear_order.yaml")

def load_recycle_station():
    return _load("recycle_station.yaml")

def load_recycle_cooperation():
    return _load("recycle_cooperation.yaml")

def load_recycle_station_sign():
    return _load("recycle_station_sign.yaml")

def load_recycle_station_map():
    return _load("recycle_station_map.yaml")

def load_recycle_app_operation_center():
    return _load("recycle_app_operation_center.yaml")

def load_recycle_app_order():
    return _load("recycle_app_order.yaml")

def load_recycle_station_clue():
    return _load("recycle_station_clue.yaml")

def load_recycle_clear_order_weigher():
    return _load("recycle_clear_order_weigher.yaml")

def load_recycle_clear_order_driver():
    return _load("recycle_clear_order_driver.yaml")

# === Member tag 模块 ===
def load_member_tag_create():
    return _load("member_tag_create.yaml")

def load_member_tag_delete():
    return _load("member_tag_delete.yaml")

def load_member_tag_get():
    return _load("member_tag_get.yaml")

def load_member_tag_list():
    return _load("member_tag_list.yaml")

def load_member_tag_page():
    return _load("member_tag_page.yaml")

def load_member_tag_update():
    return _load("member_tag_update.yaml")

# === Member level 模块 ===
def load_member_level_create():
    return _load("member_level_create.yaml")

def load_member_level_update():
    return _load("member_level_update.yaml")

def load_yaml(filename: str) -> dict:
    """按文件名从 Date/ 目录加载 YAML（含后缀）"""
    return _load(filename)

# === order 模块 ===
def load_station_order():
    return _load("station_order_submit.yaml")

def save_yaml(filename: str, data: dict) -> None:
    """将 dict 写回 Date/ 目录下的 YAML 文件（保留注释与格式）"""
    from ruamel.yaml import YAML
    path = os.path.join(DATA_DIR, filename)
    yaml_ru = YAML()
    yaml_ru.preserve_quotes = True
    yaml_ru.indent(mapping=2, sequence=4, offset=2)
    with open(path, "w", encoding="utf-8") as f:
        yaml_ru.dump(data, f)
