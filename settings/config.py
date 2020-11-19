from os.path import dirname, abspath, join, exists
import sys
from configparser import ConfigParser




base_path = dirname(abspath(__file__))
# dirname(dirname(__file__))
file_name = "settings.ini"
example_settings_filename = f"{base_path}/example_{file_name}"
config_path = join(base_path, file_name)
if not exists(example_settings_filename):
    print(f"Config file ({config_path}) not found! Exiting!")
    sys.exit(0)
if not exists(config_path):
    example_cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    example_cfg.read(example_settings_filename)
    user_input_tag = example_cfg.get("settings_ini_file", "user_input_tag")
    print("Config file not found!")
    print(f"I am trying to create {config_path}...")
    print(f"I am coping {example_settings_filename} and rename this to {config_path}")
    with open(f"{example_settings_filename}", "r", encoding="utf-8") as file, open(config_path, 'w', encoding='utf-8') as wtiten_file:
        print('\n'.join([(''.join([i + input(f"\nВведите пожалуйста {i.replace('=', '').strip()} для своей программы:\n")
                                  for i in filter(bool, string.split(user_input_tag))])
                         if user_input_tag in string and not string.startswith("user_input_tag") else string)
                         for string in iter(file.read().split('\n'))]), file=wtiten_file)

if exists(config_path):
    cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    cfg.read(config_path)
else:
    print("Config not found! Exiting!")
    print(f"I can't create {config_path}...")
    print(f"You can try cloning {base_path}/example_{file_name} to {config_path} and edit params into this")

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
