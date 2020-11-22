# -*- coding: utf-8 -*-
count_process = 4
from os.path import isfile
from os import getcwd

from flask import Flask, request, json
import git


finish_proc = []
print("Мой путь сейчас:", getcwd())
file_name = "counter"
if isfile(file_name):
    text = ""
    with open(file_name, "r", encoding='utf-8') as f:
        text += f.read().split()[0]
    text = text if bool(text) else 'None'
    print("text is ", text)
    if text.isdigit():
        if int(text) > count_process:
            from os import remove

            with open(file_name, "w", encoding='utf-8') as f:
                print(str(int(text) + 1), file=f)
            # значит это последний запущенный процесс
            # удаляем файл счетчика

            # remove(file_name)
            print('-----')

        else:
            with open(file_name, "w", encoding='utf-8') as f:
                print(str(int(text) + 1), file=f)
    else:
        with open(file_name, "w", encoding='utf-8') as f:
            print("1", file=f)
else:
    print('******7&&&&&&&')
    with open(file_name, "w", encoding='utf-8') as f:
        print("1", file=f)

__name__ = "sub.programm"
if isfile(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        text = str(f.read()).split()[0]
        if text != '1':
            __name__ = "sub.programm"
        else:
            __name__ = "__main__"
        print([text])
else:
    __name__ = "sub.programm"


def callback_func(*args, **kwargs):
    print('---------------------------------')
    print('callback_func', )
    print(args)
    print(kwargs)
    finish_proc.append(args[0])
    print('---------------------------------')


def error_callback_func(*args, **kwargs):
    print('---------------------------------')
    print('error_callback_func', )
    print(args)
    print(kwargs)
    finish_proc.append(1)
    print('---------------------------------')


def find_parh_to_dit(target_dir_name, path=None):
    from os import getcwd
    from os.path import split as os_split, exists, join as os_join

    path = path or getcwd()
    old_path = ''
    while target_dir_name not in path:
        if exists(os_join(path, target_dir_name)):
            path = os_join(path, target_dir_name)
            break
        now_dir = os_split(path)[1]
        path = os_split(path)[0]
        if old_path == path:
            break
        old_path = path
        print(path, now_dir)
    else:
        all_path, end_dir = os_split(path)
        while end_dir != target_dir_name:
            now_dir = path[1]
            path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    return path


def is_valid_signature(x_hub_signature, data, private_key):
    import hmac
    import hashlib

    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    if x_hub_signature:
        hash_algorithm, github_signature = x_hub_signature.split('=', 1)
        algorithm = hashlib.__dict__.get(hash_algorithm)
        encoded_key = bytes(private_key, 'latin-1')
        mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
        print('проверка подлинности почти замершилась')
        return hmac.compare_digest(mac.hexdigest(), github_signature)


if __name__ == '__main__':
    print('^^^^^^^^^')
    import os

    print("переменные окружения", os.environ)
    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info', 'fff', "end_work"]
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}, "new_event_from_vk", "finish_listen"]

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

    print(1)

    hostname = os.environ.get('HOST_NAME', "")
    wsgi_module = os.environ.get('WSGI_MODULE', None)
    # print(find_parh_to_dit('hooks'))

    print(2, hostname, "pythonanywhere" in str(hostname), wsgi_module)
    if "pythonanywhere" in str(hostname) and wsgi_module:
        git_path = find_parh_to_dit('.git')
        print(git_path)
        with open(os.path.join(git_path, "hooks", "post-merge"), "w", encoding="utf-8") as file:
            run_file_path = f"""/var/www/{wsgi_module}.py"""
            print(f"""#!/bin/sh\nkillall uwsgi\ntouch {run_file_path}""", file=file)
        os.system(f"chmod +x {run_file_path}")
    print(3)
    from multiprocessing import Pool, cpu_count, Manager

    print(3.5)
    # =======! initialization !=======
    pool = Pool(processes=count_process)
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
    # chains_mps = {(i if type(i) != dict else list(i.keys())[0]): [print(i), (
    #     Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])][1]
    #               for i in chains_mps}
    print(4.5)
    users_data = ['admins', 'developers']
    # users_data= {admins: {admin_id: session: bool, ...}, developers: {dev_id: bool, ...}, ...}
    # users_data = {i: Manager().dict() for i in users_data}
    print(5)
    # =======! Создание общих частей для классов-родителей !=======
    try:
        BaseClass.common_start(queues=chains_mps, types=types)
        VkBase.common_start()
    except Exception:
        pass
    print(6)
    # =======! Start working !=======
    r = [pool.apply_async(i.start, kwds={'vip_users': users_data, 'queues': chains_mps, 'types': types},
                          error_callback=error_callback_func, callback=callback_func) for i in [VkListen, VkSending]]
    r.extend([pool.apply_async(i.start, kwds={'queues': chains_mps, 'types': types},
                               error_callback=error_callback_func, callback=callback_func) for i in
              [ProcessingMsg, ControlDB]])
    [i.ready() for i in r]
    print(7)


    # sleep(20)
    # ended_work(chains_mps)
    # while True:
    #     sleep(1)
else:
    print('90988888***********', __name__)
    chains_mps = None
    # app = None


def ended_work(chains_mps):
    print(chains_mps)
    if chains_mps:
        chains_mps['finish_listen'].put('end')
        chains_mps['send'].put(("end_work", []))
        chains_mps['listen'].put(("end_work", []))
        chains_mps['proc'][0].put(("end_work", []))
        chains_mps['db'][0].put(("db", []))
        print('funish ended_work')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def flask_processing():
    print('909090----')
    # if type(chains_mps) != list:
    # data = json.loads(request.data)
    # chains_mps['new_event_from_vk'].put(data)


@app.route('/git_pull', methods=['POST'])
def webhook():
    try:
        import psutil
        print(*(p.name() for p in psutil.process_iter()))
    except Exception as e:
        print("Не получилось получить список процессов", e)
    if request.method == 'POST' and webhook.chains_mps_loc:
        import os
        from settings.config import cfg
        from time import time


        x_hub_signature = request.headers.get('X - Hub - Signature')
        w_secret = cfg.get("git", "secret_key_git")
        print('w_secret', w_secret)
        if w_secret and not is_valid_signature(x_hub_signature, request.data, w_secret):
            print('pulling........')
            ended_work(webhook.chains_mps_loc)
            repo = git.Repo()
            origin = repo.remotes.origin
            if os.path.isfile(file_name):
                os.remove(file_name)
            start_time = time()
            while len(finish_proc) < 4:
                if time() - start_time > 70:
                    break
            print("****", finish_proc)
            origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

setattr(webhook, "chains_mps_loc", chains_mps)

if __name__ != '__main__':
    app = None


print('----------------------------------------------', app)