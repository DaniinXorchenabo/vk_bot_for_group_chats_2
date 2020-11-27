# -*- coding: utf-8 -*-

# if True or __name__ == '__main__':
#     with open("main_with_flask.py", 'r', encoding='utf-8') as file:
#         text = file.read()
#
#     from time import sleep
#     print('******************')
#     while True:
#         sleep(1)

# -------------------------------------------
with open("main_with_flask.py", 'r', encoding='utf-8') as file:
    text = file.read()

exec(text)
try:
    print(app)
    app.run()
except Exception as e:

    print(e)

try:
    print(ee)
except Exception as e:

    print(e)
