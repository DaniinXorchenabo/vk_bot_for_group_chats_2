# -*- coding: utf-8 -*-

from start.starting_funcs import *


set_name_param()
print("Мой путь сейчас:", getcwd())

if __name__ == '__main__':
    flask_main()
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
# if app:
#     app.run()
print('----------------------------------------------', app)
