# -*- coding: utf-8 -*-

from base.base_libs import *


COUNT_PROCESS = 4
FILE_COUNTER_NAME = 'counter'
finish_proc = []


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
    """
    Проверка, пришёл ли запрос с Гитхаб'а
    :param x_hub_signature:
    :param data:
    :param private_key:
    :return:
    """
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


def ended_work(chains_mps):
    print(chains_mps)
    if chains_mps:
        chains_mps['finish_listen'].put('end')
        chains_mps['send'].put(("end_work", []))
        chains_mps['listen'].put(("end_work", []))
        chains_mps['proc'][0].put(("end_work", []))
        chains_mps['db'][0].put(("end_work", []))
        print('finish ended_work')

def create_post_git_pull_file():
    from os import environ, system

    hostname = environ.get('HOST_NAME', "")
    wsgi_module = environ.get('WSGI_MODULE', None)
    # print(find_parh_to_dit('hooks'))

    # print(2, hostname, "pythonanywhere" in str(hostname), wsgi_module)
    if "pythonanywhere" in str(hostname) and wsgi_module:
        git_path = find_parh_to_dit('.git')
        print(git_path)
        with open(join(git_path, "hooks", "post-merge.sample"), "w", encoding="utf-8") as file:
            run_file_path = f"""/var/www/{wsgi_module}.py"""
            text = [
                "!/bin/sh",
                f"if [[ -f {join(getcwd(), FILE_COUNTER_NAME)} ]]",
                f"then\nrm {join(getcwd(), FILE_COUNTER_NAME)}\nfi",
                # "killall uwsgi\n",
                "touch {run_file_path}"
            ]
            print("\n".join(text), file=file)
        system(f"chmod +x {run_file_path}")