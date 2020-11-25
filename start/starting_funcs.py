# -*- coding: utf-8 -*-

from base.libs import *

def set_name_param():
    global __name__
    if isfile(FILE_COUNTER_NAME):
        text = ""
        with open(FILE_COUNTER_NAME, "r", encoding='utf-8') as f:
            text += f.read().split()[0]
        text = text if bool(text) else 'None'
        print("text is ", text)
        if text.isdigit():
            if int(text) > COUNT_PROCESS:
                from os import remove

                with open(FILE_COUNTER_NAME, "w", encoding='utf-8') as f:
                    print(str(int(text) + 1), file=f)
                # значит это последний запущенный процесс
                # удаляем файл счетчика

                # remove(file_name)
                print('-----')

            else:
                with open(FILE_COUNTER_NAME, "w", encoding='utf-8') as f:
                    print(str(int(text) + 1), file=f)
        else:
            with open(FILE_COUNTER_NAME, "w", encoding='utf-8') as f:
                print("1", file=f)
    else:
        print('******7&&&&&&&')
        with open(FILE_COUNTER_NAME, "w", encoding='utf-8') as f:
            print("1", file=f)

    __name__ = "sub.programm"
    if isfile(FILE_COUNTER_NAME):
        with open(FILE_COUNTER_NAME, "r", encoding='utf-8') as f:
            text = str(f.read()).split()[0]
            if text != '1':
                __name__ = "sub.programm"
            else:
                __name__ = "__main__"
            print([text])
    else:
        __name__ = "sub.programm"


def base_main():
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
    pool = Pool(processes=COUNT_PROCESS or cpu_count())
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


def flask_main():
    create_post_git_pull_file()
    base_main()