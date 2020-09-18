from db.db_controller import ControlDB
from db.models import *
from collections import Counter
from base.base_libs import *

if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split
    from random import randint
    from time import ctime

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)


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
    print([i for i in Admins.select()])
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


@ControlDB.command('/erease', pr=0)
@db_session
def erease_memoty(cls, comamnd, event, *args_q, queues=dict(), **kwargs_q):
    id_chat = event['object']['peer_id']

    if not Chat.exists(id=id_chat):
        Chat(id=id_chat)
        flush()
    # print('очищение помяти БД')
    try:
        delete(w for w in Words if w.chat_id == id_chat)
        Chat[id_chat].delete()
        ans = 'Память была успешно очищена😎'
    except Exception as e:
        print('произошла ошибка при очищении памяти чата', id_chat, ":", e)
        ans = 'При очищении память произошла какая-то ошибка👉🏻👈🏻😅'
    cls.put_send('text', ans, event, queues=queues)


@ControlDB.command('/stat', pr=0)
@db_session
def get_sts_for_chat(cls, comamnd, event, *args_q, queues=dict(), **kwargs_q):
    id_chat = event['object']['peer_id']
    if not Chat.exists(id=id_chat):
        Chat(id=id_chat)
        flush()
    ans = f'📝 Количество использованных слов: {Chat[id_chat].count_words}\n🔢 ID чата: {id_chat}'
    cls.put_send('text', ans, event, queues=queues)


@ControlDB.command('/get_admins', pr=0)
@db_session
def get_admins(cls, *args_q, queues=dict(), **kwargs_q):
    admins = [adm.id for adm in Admins.select()]
    print("@ControlDB.command('/get_admins', pr=0)", admins)
    cls.put_send('inner_info', 'set_admins', admins, queues=queues)

@ControlDB.command('/get_developers', pr=0)
@db_session
def get_developers(cls, *args_q, queues=dict(), **kwargs_q):
    developers = [dev.id for dev in Developers.select()]
    # print("@ControlDB.command('/get_admins', pr=0)", developers)
    cls.put_send('inner_info', 'set_developers', developers, queues=queues)

@ControlDB.command('/add_admin', pr=0)
@db_session
def add_admin(cls, command, data, peer_id, *args_q, queues=dict(), **kwargs_q):
    # print('---------------', [peer_id])
    if not Admins.exists(id=int(peer_id)):
        Admins(id=int(peer_id))
        commit()
    # print(peer_id)

@ControlDB.command('/add_developer', pr=0)
@db_session
def add_developer(cls, command, data, peer_id, *args_q, queues=dict(), **kwargs_q):
    # print('---------------', [peer_id])
    if not Developers.exists(id=int(peer_id)):
        Developers(id=int(peer_id))
        commit()
    # print(peer_id)

@ControlDB.command('/del_me', pr=0)
@db_session
def del_me_admin(cls, command, data: dict,  peer_id, *args_q, queues=dict(), **kwargs_q):
    if Admins.exists(id=int(peer_id)):
        Admins[peer_id].delete()
        commit()
    cls.put_db('content', '/get_admins', 'useless data', queues=queues, pr=0)
    cls.put_send('text', 'теперь вы больше не администратор', data, queues=queues)


@ControlDB.command('/dev_del_me', pr=0)
@db_session
def del_me_developer(cls, command, data: dict,  peer_id, *args_q, queues=dict(), **kwargs_q):
    if Developers.exists(id=int(peer_id)):
        Developers[peer_id].delete()
        commit()
    cls.put_db('content', '/get_developers', 'useless data', queues=queues, pr=0)
    cls.put_send('text', 'вы удалены из разработчиков', data, queues=queues)


@ControlDB.command('/get_list_admins', pr=0)
@db_session
def get_list_admins(cls, command, data: dict,  peer_id_useless, *args_q, queues=dict(), **kwargs_q):
    ans = f'список админов из базы данных:\n'
    ans += '\n'.join([str(adm.id) for adm in Admins.select()])
    cls.put_send('text', ans, data, queues=queues)


@ControlDB.command('/get_list_developers', pr=0)
@db_session
def get_list_developers(cls, command, data: dict,  peer_id_useless, *args_q, queues=dict(), **kwargs_q):
    ans = f'список разработчиков из базы данных:\n'
    ans += '\n'.join([str(dev.id) for dev in Developers.select()])
    cls.put_send('text', ans, data, queues=queues)


@ControlDB.command('/del_all_admins', pr=0)
@db_session
def del_all_admins(cls, command, data: dict,  peer_id_useless, *args_q, queues=dict(), **kwargs_q):
    delete((i for i in Admins.select()))
    commit()
    ans = f'все админы были успешно удалены и БД'
    cls.put_send('text', ans, data, queues=queues)