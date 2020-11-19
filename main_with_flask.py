# -*- coding: utf-8 -*-

def error_callback_func(*args, **kwargs):
    print('---------------------------------')
    print('error_callback_func', )
    print(args)
    print(kwargs)
    print('---------------------------------')

def find_parh_to_dit(target_dir_name):
    from os import getcwd
    from os.path import split as os_split, exists, join as os_join

    path = getcwd()
    while target_dir_name not in path:
        if exists(os_join(path, target_dir_name)):
            path = os_join(path, target_dir_name)
            break
        now_dir = os_split(path)[1]
        path = os_split(path)[0]
        print(path, now_dir)
    else:
        all_path, end_dir = os_split(path)
        while end_dir != target_dir_name:
            now_dir = path[1]
            path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    return path

if __name__ == '__main__':

    from flask import Flask, request, json
    import git

    app = Flask(__name__)

    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info', 'fff']
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}, "new_event_from_vk"]




    # import importlib
    # import nltk.collections
    # importlib.import_module("base.base_libs.py")
    # import json
    # from requests import request

    try:
        from base.base_libs import *
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
        from base_libs import *
        from base_class import BaseClass
        from vk_base_class import VkBase
        # from vk.vk_commands import *
        from processing_messenges import ProcessingMsg
        from db_controller import ControlDB
        from vk_listen import VkListen
        from vk_sending import VkSending
        from config import cfg

    @app.route('/', methods=['POST'])
    def flask_processing():
        print('909090----')
        if type(chains_mps) != list:
            data = json.loads(request.data)
            chains_mps['new_event_from_vk'].put(data)


    @app.route('/git_pull', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('path/to/git_repo')
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400


    import socket

    hostname = socket.gethostname()
    print(find_parh_to_dit('hooks'))
    git_path = find_parh_to_dit('.git')
    if "pythonanywhere" in str('hostname'):
        with open(os.path.join(git_path, "hooks", "post-merge"), "w", encoding="utf-8") as file:
            run_file_path = f"""/var/www/{hostname.replace(
                '.pythonanywhere.com', '').replace('https://', '').replace('http://', '').replace('.', '').replace(
                '/', '').split(':')[0]}_pythonanywhere_com_wsgi.py"""
            print(f"""#!/bin/sh\ntouch {run_file_path}""", file=file)
        os.system(f"chmod +x {run_file_path}")

    from multiprocessing import Pool, cpu_count, Manager

    # =======! initialization !=======
    pool = Pool(processes=2)
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
    while True:
        sleep(1)
