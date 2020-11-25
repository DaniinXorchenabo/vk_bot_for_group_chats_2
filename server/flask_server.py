# -*- coding: utf-8 -*-

from flask import Flask, request, json
import git

from base.libs import *


app = Flask(__name__)


@app.route('/test2')
def flask_test2():
    return "test1 _ 2"


@app.route('/test1')
def flask_test():
    import os
    import sys

    print('Restarting program. Arguments {}'.format(sys.argv))
    python = sys.executable
    # os.execl(python, python, * sys.argv)
    return "test1 _ 1"


@app.route('/', methods=['POST'])
def flask_processing():
    print('909090----')
    # if type(chains_mps) != list:
    # data = json.loads(request.data)
    # chains_mps['new_event_from_vk'].put(data)


@app.route('/git_pull', methods=['POST'])
def webhook():
    global chains_mps
    if request.method == 'POST' and chains_mps:
        from os import remove
        from settings.config import cfg
        from time import time

        x_hub_signature = request.headers.get('X - Hub - Signature')
        w_secret = cfg.get("git", "secret_key_git")
        # print('w_secret', w_secret)
        if w_secret and not is_valid_signature(x_hub_signature, request.data, w_secret):
            print('pulling........')
            ended_work(chains_mps)
            repo = git.Repo()
            origin = repo.remotes.origin
            if isfile(FILE_COUNTER_NAME):
                remove(FILE_COUNTER_NAME)
            start_time = time()
            finish_proc_1 = []
            while len(finish_proc_1) < 4:
                if not chains_mps['end_work_for_main'].empty():
                    finish_proc_1.append(chains_mps['end_work_for_main'].get())
                if time() - start_time > 70:
                    break
            print("****", finish_proc_1)
            origin.pull()
            print('---*****')

            # print('выход.........................................................')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
