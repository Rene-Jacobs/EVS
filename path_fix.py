import os
import sys


def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_authoritative_list_path():
    base_dir = get_base_dir()
    return os.path.join(base_dir, "data", "AuthoritativeEntityList.csv")
