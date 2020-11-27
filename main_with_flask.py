# -*- coding: utf-8 -*-

from start.starting_funcs import *


__name__ = set_name_param()
print("Мой путь сейчас:", getcwd())
print(__name__)
if __name__ == '__main__':
    app = None
    create_post_git_pull_file()
    global types, chains_mps
    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info', "end_work"]
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}, "new_event_from_vk", "finish_listen",
                  "end_work_for_main"]
    users_data = ['admins', 'developers']

    try:
        from base.base_class import BaseClass
        from vk.vk_base_class import VkBase
        # from vk.vk_commands import *
        from processing.processing_messenges import ProcessingMsg
        from db.db_controller import ControlDB
        from vk.vk_listen import VkListen
        from vk.vk_sending import VkSending
        from settings.config import cfg
    except Exception as e:
        print('произошла ошибка', e)
        print('попытка исправить')
        import sys
        import os

        my_path = os.getcwd()
        dirs = [os.path.join(my_path, i) for i in os.listdir(my_path)]
        sys.path.extend(dirs)
        from base_class import BaseClass
        from vk_base_class import VkBase
        # from vk.vk_commands import *
        from processing_messenges import ProcessingMsg
        from db_controller import ControlDB
        from vk_listen import VkListen
        from vk_sending import VkSending
        from config import cfg

    from multiprocessing import Pool, cpu_count, Manager

    print(3.5)
    # =======! initialization !=======
    try:
        pool = Pool(processes=COUNT_PROCESS or cpu_count())
    except Exception as e:
        print('ошибка при создании многопроцессорности:', e)
    # очередь = [(type: str, content: typle), ...]
    #   type='func':    очередь = [('func', (func, args: list, kwargs: dict)), ...]
    #   type='ev':   очередь = [('ev', (type_ev:str, data:dict, func, args, kwargs)), ...] (ev - событие)
    #   type='text':   очередь = [('text', (text: str, data: dict)), ...]  data - словарь из пришедшего сообщения
    #   text='???':     очередь = [('content', (type:str, (data), peer_id:int, )), ...]
    #   type='cooking_msg'      = [('cooking_msg', msg: dict), ...]
    #   type='change_param'      = [('change_param', (peer_id, text, data: dict)), ...] data - словарь с обновленными параметрами
    #   type='inner_info'        = [('inner_info', (type, data)), ...]
    #       proc - для отправки в класс обработки сообщений
    #       db - для отправки в класс базы данных
    #       type_ev = [new_msg - новое сообщение]

    print(4)
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): [print(i), (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])][1]
                  for i in chains_mps}
    print(4.5)
    # users_data= {admins: {admin_id: session: bool, ...}, developers: {dev_id: bool, ...}, ...}
    users_data = {i: Manager().dict() for i in users_data}
    print(5)
    # =======! Создание общих частей для классов-родителей !=======
    BaseClass.common_start(queues=chains_mps, types=types)
    VkBase.common_start()
    print(6)
    # =======! Start working !=======
    r = [pool.apply_async(i.start, kwds={'vip_users': users_data, 'queues': chains_mps, 'types': types},
                          error_callback=error_callback_func, callback=callback_func) for i in [VkListen, VkSending]]
    r.extend([pool.apply_async(i.start, kwds={'queues': chains_mps, 'types': types},
                               error_callback=error_callback_func, callback=callback_func) for i in
              [ProcessingMsg, ControlDB]])
    [i.ready() for i in r]
    # from inspect import getsource
    # code = getsource(flask_main).split('\n')
    # count_tabs = code[0].split('def')[0].count(' ') + 4
    # code = "\n".join([''.join(list(i)[count_tabs :]) for i in code[1:]])
    # exec(code)
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
ee = "11"
print('----------------------------------------------', app)
