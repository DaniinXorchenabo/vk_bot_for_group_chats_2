# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join, exists
import sys
from configparser import ConfigParser




base_path = dirname(abspath(__file__))
# dirname(dirname(__file__))
config_path = join(base_path, "settings.ini")
if exists(config_path):
    cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    cfg.read(config_path)
else:
    print("Config not found! Exiting!")
    sys.exit(1)

def save_change_in_cinfig_file():
    with open(config_path, "w") as config_file:
        cfg.write(config_file)


# class Config():
#
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     config_path = os.path.join(base_path, "settings.ini")
#     cfg = None
#
#     @classmethod
#     def start(cls):
#         if os.path.exists(cls.config_path):
#             cls.cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
#             cls.cfg.read(cls.config_path)
#         else:
#             print("Config not found! Exiting!")
#             sys.exit(1)
#
#     @classmethod
#     def change_init_file(cls, *args):
#         cls.cfg.set(*args)
