from base.base_class import *
from settings.config import cfg
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent,
    VkBotEventType
)


class VkBase(BaseClass):

    vk_session = None

    func_for_com = dict()  # {str: processing_func, ...}
    rec_com = dict()  # {recognize_func: (name_com: str, processing_func), ...}
    all_commands = ['/new_msg']
    DBless_com = [[], []]  # [[команды без аргументов], [команды с аргументами]]
    find_main_com = dict()  # {второстепенная команда: основное название команды}
    # [[[команды, которые не принимают аргументов], [команды с аргументами]], ...]
    # списиок списков. первый индекс - приоритетность запроса
    prior_com = []  # type: list[list[(str), (str)]]
    admin_com = []  # команды, доступные только из админки
    developer_com = []  # команды, доступные только для разработчика
    help_command = ''
    admins = dict()  # {peer_id: seeeion}
    developers = dict()  # {peer_id: seeeion}

    list_keys = ['user_id', "random_id", "peer_id", "domain",
                 "chat_id", "user_ids", "message", "lat", "long",
                 "attachment", "reply_to", "forward_messages",
                 "sticker_id", "group_id", "keyboard", "payload",
                 "dont_parse_links", "disable_mentions", "intent",
                 "subscribe_id"]

    # =======! Started !=======
    @classmethod
    def start_base_vk(cls):
        cls.vk_session = VkApi(token=cfg.get("vk", "token"))
        cls.all_commands += list(cls.func_for_com.keys())

    @classmethod
    def child_start(cls, queues, users, *ar_cl, **kw_cl):
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
        :param db_acc: False - если для команды не требуется доступа к БД.
                    Число с 0 - уровень приоритетности запроса к БД
        """
        def decorator(func):
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
                cls.create_msg(res, )

            cls.func_for_com.update({i: wrapped for i in [com_name] + duple})
            cls.find_main_com.update({com_name: i for i in [com_name] + duple})
            cls.rec_com.update({i: (com_name, wrapped) for i in rec_f})
            if db_acc:
                cls.priority_list_created(db_acc, [com_name] + duple, it_is_part)
            else:
                cls.DBless_com[it_is_part] += [com_name] + duple
            return wrapped

        return decorator

    @classmethod
    def priority_list_created(cls, pr, elements, it_is_part):
        if len(cls.prior_com) <= pr:
            cls.prior_com += [[], []] * (pr - len(cls.prior_com) + 1)
        cls.prior_com[pr][it_is_part] += (elements if type(elements) == list else [elements])

    @classmethod
    def create_msg(cls, text, *args, **kwargs):
        pass


from vk.vk_commands import *

if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
