if __name__ == '__main__':
    from db.db_controller import ControlDB
    from db.models import *
    from os import getcwd
    from os.path import split as os_split
    from random import randint
    from db.models import *
    from collections import Counter
    from time import ctime

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)

from db.db_controller import ControlDB
from db.models import *
from collections import Counter
from base.base_libs import *


@ControlDB.command('/new_msg', pr=-1)
@db_session
def db_working_with_new_msg(cls, comamnd, data, id_chat, *args_q, queues=dict(), **kwargs_q):
    # print("работает обработка нового сообщения", id_chat, text_msg, *other)
    # text_msg  =  [({start_w: {val: count, ...}, ...} {word: {word_val: count, ...}, ...}), ...]
    start_w, simple_w = data
    if not Chat.exists(id=id_chat):
        Chat(id=id_chat)
        flush()

    # добавляем слова в БД, если их там еще нет. Если стартовое слово не являлось до этого стартовым, то исправляем это
    chat_now = Chat[id_chat]
    for words, other_params in [(start_w, {'chat': chat_now}), (simple_w, dict())]:
        if bool(other_params):
            [Words[id_chat, w].set(chat=chat_now) for w in words if Words.exists(chat_id=id_chat, word=w)]
            # присвоить сущность чата слову, если у него ее нет, но слово уже существует
        [Words(chat_id=id_chat, word=w, **other_params) for w in words if not Words.exists(chat_id=id_chat, word=w)]
    flush()

    min_d, max_d = (start_w, simple_w) if len(start_w) < len(simple_w) else (simple_w, start_w)
    min_d = {key: (val + max_d.get(key) if max_d.get(key) else val) for key, val in min_d.items()}
    max_d.update(min_d)
    # print('все новые слова внесены в БД')
    for key, vals in max_d.items():
        # print('start pr', key, vals)
        w = Words[id_chat, key]
        w.val = arr = set(w.val + [Words[id_chat, w_val] for w_val in vals.keys()])
        # print('$$$$')
        w.len_vals = len(arr)
        w.count_vals += sum(vals.values())
        # print(')))))')
        chat_now.count_words += sum(vals.values())
        w.vals_dict = dict(Counter(w.vals_dict) + Counter(vals))
        # print('end pr')
    commit()
    print('end write in DB--------------------------------------')


@ControlDB.command('/gen', pr=-2)
@db_session
def generate_new_msg(cls, comamnd, event, *args_q, queues=dict(), **kwargs_q):
    id_chat = event['object']['peer_id']

    # print('получение /gen из БД')
    if Chat.exists(id=id_chat) and Chat[id_chat].count_words > 0:
        chat_now = Chat[id_chat]
        max_len = randint(1, 50)
        ans = []
        entity = None
        while True:
            if max_len < 0 and not entity:
                break
            elif max_len >= 0 and not entity:
                # print(chat_now.start_words)
                entity = list(chat_now.start_words)[randint(0, len(chat_now.start_words) - 1)]
                # print(entity)
                if bool(ans) and ans[-1] not in list('.!?'):
                    ans.append('.')

            ans.append(entity.word)
            max_len -= 1
            if max_len < -500:
                break
            # print('*********----')
            entity = (None if entity.len_vals < 1 else list(entity.val)[randint(0, len(entity.val) - 1)])
            # print('*********----', entity)
    else:
        if not Chat.exists(id=id_chat):
            Chat(id=id_chat)
            # flush()
        ans = 'Я не могу писать, если не знаю слов :c'
    print('***44434-20-34', cls, hasattr(cls, 'put_proc'))
    cls.put_proc('content', '/gen', (ans, event), pr=0, queues=queues)
    print('*______))))))))))))')
