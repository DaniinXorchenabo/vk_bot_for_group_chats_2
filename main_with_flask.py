# -*- coding: utf-8 -*-

from start.starting_funcs import *

old_name = __name__
__name__ = set_name_param()
print("Мой путь сейчас:", getcwd())
print(__name__)
if __name__ == '__main__':
    app = None
    create_post_git_pull_file()

    from inspect import getsource
    code = getsource(flask_main).split('\n')
    count_tabs = code[0].split('def')[0].count(' ') + 4
    code = "\n".join([''.join(list(i)[count_tabs :]) for i in code[1:]])
    exec(code)

else:
    print('90988888***********', __name__)
    chains_mps = None
    # app = None

try:
    app = None
    from server.flask_server import *

except Exception as e:
    print("не получилось создать app = Flask(__name__)", e)
    app = None

if __name__ != '__main__':
    app = None
if app and old_name == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '-start_server':
        print('---------------------------------------------', sys.argv)
        app.run()
ee = "11"
print('----------------------------------------------', app)
