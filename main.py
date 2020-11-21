# -*- coding: utf-8 -*-

def error_callback_func(*args, **kwargs):
    print('---------------------------------')
    print('error_callback_func', )
    print(args)
    print(kwargs)
    print('---------------------------------')


if __name__ == '__main__':
    # import importlib
    # import nltk.collections
    # importlib.import_module("base.base_libs.py")

    try:
        from base.base_libs import *
        from base.base_class import BaseClass
        from vk.vk_base_class import VkBase
        # from vk.vk_commands import *
        from processing.processing_messenges import ProcessingMsg
        from db.db_controller import ControlDB
        from vk.vk_listen import VkListen
        from vk.vk_sending import VkSending
    except Exception as e:
        print('произошла ошибка', e)
        print('попытка исправить')
        import sys
        import os

        my_path = os.getcwd()
        dirs = [os.path.join(my_path, i) for i in os.listdir(my_path)]
        sys.path.extend(dirs)
        from base_libs import *
        from base_class import BaseClass
        from vk_base_class import VkBase
        # from vk.vk_commands import *
        from processing_messenges import ProcessingMsg
        from db_controller import ControlDB
        from vk_listen import VkListen
        from vk_sending import VkSending
    from multiprocessing import Pool, cpu_count, Manager


    # =======! initialization !=======
    pool = Pool(processes=4)
    # очередь = [(type: str, content: typle), ...]
    #   type='func':    очередь = [('func', (func, args: list, kwargs: dict)), ...]
    #   type='ev':   очередь = [('ev', (type_ev:str, data:dict, func, args, kwargs)), ...] (ev - событие)
    #   type='text':   очередь = [('text', (text: str, data: dict)), ...]  data - словарь из пришедшего сообщения
    #   text='???':     очередь = [('content', (type:str, (data), peer_id:int, )), ...]
    #   type='cooking_msg'      = [('cooking_msg', msg: dict), ...]
    #   type='change_param'      = [('change_param', (peer_id, text, data: dict)), ...] data - словарь с обновленными параметрами
    #   type='inner_info'        = [('inner_info', (type, data)), ...]
    #   type='end_work'          = [("end_work", []), ...]
    #       proc - для отправки в класс обработки сообщений
    #       db - для отправки в класс базы данных
    #       type_ev = [new_msg - новое сообщение]

    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info', 'fff', "end_work"]
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}, "new_event_from_vk", "finish_listen"]
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])
        for i in chains_mps}

    users_data = ['admins', 'developers']
    # users_data= {admins: {admin_id: session: bool, ...}, developers: {dev_id: bool, ...}, ...}
    users_data = {i: Manager().dict() for i in users_data}


    # =======! Создание общих частей для классов-родителей !=======
    BaseClass.common_start(queues=chains_mps, types=types)
    VkBase.common_start()
    # =======! Start working !=======
    r = [pool.apply_async(i.start, kwds={'vip_users': users_data, 'queues': chains_mps, 'types': types},
                          error_callback=error_callback_func) for i in [VkListen, VkSending]]
    r.extend([pool.apply_async(i.start, kwds={'queues': chains_mps, 'types': types},
                               error_callback=error_callback_func) for i in [ProcessingMsg, ControlDB]])
    [i.ready() for i in r]
    sleep(20)
    chains_mps['finish_listen'].put('end')
    print('----')
    while True:
        sleep(1)
