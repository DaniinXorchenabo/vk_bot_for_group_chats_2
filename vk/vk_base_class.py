from base.base_class import *
from settings.config import cfg
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent,
    VkBotEventType
)
from vk.vk_buttons import *


class VkBase(BaseClass):
    vk_session = None

    func_for_com = dict()  # {str: processing_func, ...} содержит все команды и функции их обработки

    # содержит функцию определения команды, название команды и функцию ее обраьотки
    rec_com = dict()  # {recognize_func: (name_com: str, processing_func), ...}
    all_commands = ['/new_msg']  # список всех команд

    # список всех команд, не требующих доступа к БД.
    DBless_com = [[], []]  # [[команды без аргументов], [команды с аргументами]]

    # позволяет найти имя главной команды по названию второстепенной (пример: find_main_com['помоги'] = "/help")
    find_main_com = dict()  # {второстепенная команда: основное название команды}

    # [[[команды, которые не принимают аргументов], [команды с аргументами]], ...]
    # списиок списков. первый индекс - приоритетность запроса
    prior_com_proc = []  # type: list[list[(str), (str)]]  # команды, отправляемые сначала на обработку
    prior_com_db = []  # type: list[list[(str), (str)]]  # Команды, идущие сразу в БД
    """
    [
     [[str, ...], [str, ...]], ...
    ]
    prior_com_db[приоритетность команды][0 - если просто команда; 1 - если команда с аргументами]
    """
    admin_com = []  # команды, доступные только из админки
    developer_com = []  # команды, доступные только для разработчика
    help_command = ''
    admins = dict()  # {peer_id: seeeion (bool), ...}
    developers = dict()  # {peer_id: seeeion (boop), ...}

    # =======! Started !=======

    @classmethod
    def common_start(cls, **kw_init):
        """
        запускается в начальном потоке, чтобы не выполнять одинаковые операции в начале
        на разных потоках
        """
        if not cls.vk_session:
            cls.start_base_vk()

    @classmethod
    def start_base_vk(cls):
        cls.vk_session = VkApi(token=cfg.get("vk", "token"))
        cls.all_commands += list(cls.func_for_com.keys())

    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), users=dict(), **kw_cl):
        if not cls.vk_session:
            cls.start_base_vk()

    # =======! msg processing !=======
    @classmethod
    def commands(cls, com_name: str, *args, duple: list = [], it_is_part=0, rec_f: list = [], db_acc=False, **kwargs):
        """
        :param com_name: стандартное обозначение команды
        :param args: остальные параметры
        :param duple: дублирубщие ключевые слова для com_name
        :param it_is_part: является ли данная команда только частью сообщения (1 - если является)
        :param rec_f: функции, позволяющие определить, подходит ли сообщение под кодовое слово или нет
                        (их должно быть не много)
        :param db_acc:  False - если для команды не требуется доступа к БД.
                        (False, number: int)    первое False - быстрые вычисления, знпчит передаем запрос сразу в БД
                                                number - число с 0 - приоритетность запроса в БД
                        (num1: int, True)   num1 - запрос требует долгих предварительных вычислений, передаем запрос
                                                    в класс обработки сообщений. num1 - приоритетность запроса
                                            True - дальше передаем запрос в БД
                        (None, num2: int)   Передаем запрос сначала в БД, потом в обработку по процессам
                                            num2 - приоритет при отправке в БД
        **********************************************************************************************************
        если вы подаете db_acc = (False, number: int), то необходимо обязательно прописать
        @ControlDB.command(com_name, pr) в db/db_controller_func.py, чтобы прописать обработчик команды,
        связанной с Базой Данных. В противном случае команда не будет работать.

        если вы подаете db_acc = (num1: int, True), то необходимо обязательно прописать
        @ProcessingMsg.command(com_name, pr) в processing/processing_func.py, чтобы прописать обработчик команды
        в обработке команд. В противном случае команда не будет работать. Так же необходимо выполнить действия,
        соответствующие db_acc = (False, number: int)

        """

        def decorator(func):
            # print('from decorator', func)
            # setattr(cls, 'standart_' + func.__name__, classmethod(func))
            # new_func = getattr(cls, 'standart_' + func.__name__)
            # print('from decorator', new_func, func)

            # @wraps(func)
            def wrapped(*args_dec, **kwargs_dec):
                """
                могут быть нужны:
                    текст сообщения
                    очереди
                    id и peer_id
                    доступ к классу
                :param args_dec:
                :param kwargs_dec:
                """
                # pre_other
                res = func(cls, *args_dec, **kwargs_dec)
                return cls.create_msg(res, )

            # setattr(cls, func.__name__, classmethod(wrapped))
            # print('проверка, есть ли ' + func.__name__, hasattr(cls, func.__name__))
            # new_wrapped = getattr(cls, func.__name__ )
            # print('from decorator', func, func.__name__)
            cls.func_for_com.update({i: func for i in [com_name] + duple})
            cls.find_main_com.update({i: com_name for i in [com_name] + duple})
            cls.rec_com.update({i: (com_name, func) for i in rec_f})
            # print('*(((((((((((((((((((')
            if db_acc:
                work_st, db_st = db_acc
                if not work_st:  # если вычисления не тяжелые, то отправляем сразу в БД
                    cls.prior_com_db = cls.priority_list_created(db_st, [com_name] + duple,
                                                                 it_is_part, cls.prior_com_db)
                else:
                    cls.prior_com_proc = cls.priority_list_created(work_st, [com_name] + duple,
                                                                   it_is_part, cls.prior_com_proc)
            else:
                cls.DBless_com[it_is_part] += [com_name] + duple
            # print('_____________________________++++++++')
            return wrapped

        # print('8080808*********')
        return decorator

    @classmethod
    def priority_list_created(cls, pr, elements, it_is_part, prior_com):
        max_len = (-pr - 1 if pr < 0 else pr)
        if len(prior_com) <= max_len:
            prior_com += [[[] for i in range(2)] for _ in range(max_len - len(prior_com) + 1)]
        # print('----------------', *prior_com, '-----------------', sep='\n')
        prior_com[pr][it_is_part] += (elements if type(elements) == list else [elements])
        return prior_com

    @classmethod
    def create_msg(cls, text, *args, **kwargs):
        return text


from vk.vk_commands import *

if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
