# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys


# add your project directory to the sys.path
project_home = '/home/somethingName/vk_bot_3'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from os import getcwd, chdir, environ
print(__name__, getcwd())
chdir(project_home)
print('============================================')
print(__name__, getcwd())
try:
    pass
    # import subprocess
    # print(    returned_output = subprocess.check_output(["pgrep", "python"], shell=True).decode('utf-8', errors='ignore' ))
    # print(    returned_output = subprocess.check_output(["pgrep", "p"], shell=True,).decode('utf-8', errors='ignore' ))
except Exception as e:
    print('ошибка', e)
print('============================================')
# print(*globals().items(), sep='\n')
from os.path import join

text = 'print(Error in exec func)'
with open(join (project_home, "main_with_flask.py"), 'r', encoding='utf-8') as file:
    text = file.read()
app = '---'
old_name = __name__
__name__ = '__main__'
exec(text)
__name__ = old_name
print('============================================')
print(app)
print('============================================')
application = app


# from main_with_flask import app as application  # noqa
