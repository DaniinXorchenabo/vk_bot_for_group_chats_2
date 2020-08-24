from vk.vk_base_class import VkBase
from random import randint

@VkBase.commands('/help', duple=['помощь', "помоги", "/h"])
def get_text_help_comand(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    if not bool(cls.help_command):
        with open('settings/commands.txt', 'r', encoding='utf-8') as f:
            cls.help_command = f.read()
    cls.put_send('text', cls.help_command, event, queues=queues)


@VkBase.commands('/gen', db_acc=(-2, True))
def gen_random_text(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/gen', event, queues=queues, pr=-2)


@VkBase.commands('/erease',  duple=['/er', "очистить_память_чата", "очистить_память_беседы"], db_acc=(False, 0))
def gen_random_comand(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/erease', event, queues=queues, pr=0)


@VkBase.commands('/stat',  duple=['получить_статистику', '/st'], db_acc=(False, 0))
def gen_stat_for_chat(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/stat', event, queues=queues, pr=0)


@VkBase.commands('/get_ans_from_bot', rec_f=[lambda text: text[:4].lower() == 'бот,' and text[-1] == '?'])
def get_answer_for_your_question(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    ANSWERS = ['Да', 'Нет', 'Не знаю', 'Сложно ответить',
               'Даже мудрецы не знают ответа на этот вопрос',
               'Не важно. Съешь яблоко!', 'А почему ты спрашиваешь?',
               'Скорее нет, чем да', 'Скорее да, чем нет',
               'Что?', 'Ты пятый раз это спрашиваешь!']
    ans = ANSWERS[randint(0, len(ANSWERS)-1)]
    cls.put_send('text', ans, event, queues=queues)


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
