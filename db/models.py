from pony.orm import *

db = Database()


class Words(db.Entity):
    chat_id = Required(int)
    word = Required(str)
    key = Set('Words', reverse='val')
    val = Set('Words', reverse='key')
    len_vals = Optional(int, default=0)  # количество ключевых слов
    count_vals = Optional(int, default=0)  # кол-во встречающихся слов
    vals_dict = Optional(Json)  # dict(str, [int])  (ключевое слово: количество повторений)
    chat = Optional('Chat')
    PrimaryKey(chat_id, word)


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    count_words = Optional(int, default=0)
    keyboard = Optional(int, default=0)
    start_words = Set(Words)


class Admins(db.Entity):
    id = PrimaryKey(int)


class Developers(db.Entity):
    id = PrimaryKey(int)


def is_DB_created(path):
    from os.path import (
        join as os_join,
        isfile
    )
    from settings.config import cfg

    name_db = cfg.get("db", "name")
    if not isfile(os_join(path, "db", name_db)):
        db.bind(provider=cfg.get("db", "type"), filename=name_db, create_db=True)
        db.generate_mapping(create_tables=True)
        print('create db')
    else:
        db.bind(provider=cfg.get("db", "type"), filename=name_db)
        try:
            db.generate_mapping()
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    is_DB_created(path)
else:
    from os import getcwd

    is_DB_created(getcwd())
