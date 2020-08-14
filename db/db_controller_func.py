if __name__ == '__main__':
    from db.db_controller import ControlDB
    from db.models import *
    from os import getcwd
    from os.path import split as os_split
    from random import randint

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)

@ControlDB.command('/new_msg')
@db_session
def db_working_with_new_msg(cls, comamnd, _type, data, id_chat, *args_q, queues=dict(), **kwargs_q):
    # print("работает обработка нового сообщения", id_chat, text_msg, *other)
    # text_msg  =  [({start_w: {val: count, ...}, ...} {word: {word_val: count, ...}, ...}), ...]
    start_w, simple_w = data
    if not Chat.exists(id=id_chat):
        Chat(id=id_chat)
        flush()

    chat_now = Chat[id_chat]
    for words, other_params in [(start_w, {'chat': chat_now}), (simple_w, dict())]:
        if bool(other_params):
            pass
            # присвоить сущность чата слову, если у него ее нет, но слово уже существует
        [Words(chat_id=id_chat, word=w,
                **other_params) for w in words if not Words.exists(chat_id=id_chat, word=w)]


    flush()



    text_msg = ((StartWords, Words, text_msg[0], {'chat': Chat[id_chat]}), (Words, Words, text_msg[1], {}))
    for [entity, target_entity, part, other_params] in text_msg:
        [entity(chat_id=id_chat, word=w,
                **other_params) for w in part.keys() if not entity.exists(chat_id=id_chat, word=w)]
        flush()
    # print('все новые слова внесены в БД')
    for [entity, target_entity, part, other_params] in text_msg:
        for key, vals in part.items():
            # print('start pr', key, vals)
            w = entity[id_chat, key]
            w.val = arr = set(w.val + [target_entity[id_chat, w_val] for w_val in vals.keys()])
            # print('$$$$')
            w.len_vals = len(arr)
            w.count_vals += sum(vals.values())
            # print(')))))')
            chat_now.count_words += sum(vals.values())
            w.vals_dict = dict(Counter(w.vals_dict) + Counter(vals))
            # print('end pr')
    commit()
    # show(StartWords)
    print('end write in DB--------------------------------------', print(ctime()))
