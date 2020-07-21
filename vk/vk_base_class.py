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
    all_commands = []
    DBless_com = []
    prior_com = []  # type: list[list[str]]
    admin_com = []  # команды, доступные только из админки
    developer_com = []  # команды, доступные только для разработчика

    # =======! Started !=======
    @classmethod
    def start_base_vk(cls):
        cls.vk_session = VkApi(token=cfg.get("vk", "token"))
        cls.all_commands = list(cls.func_for_com.keys())

    @classmethod
    def child_start(cls, *ar_cl, **kw_cl):
        if not cls.vk_session:
            cls.start_base_vk()

    # =======! msg processing !=======
    @classmethod
    def commands(cls, com_name: str, *args, duple: list = [], rec_f: list = [], db_acc=False, **kwargs):
        """
        :param com_name: стандартное обозначение команды
        :param args: остальные параметры
        :param duple: дублирубщие ключевые слова для com_name
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
                # post_other
                return None

            cls.func_for_com.update({i: wrapped for i in [com_name] + duple})
            cls.rec_com.update({i: (com_name, wrapped) for i in rec_f})
            if db_acc:
                cls.priority_list_created(db_acc, [com_name] + duple)
            else:
                cls.DBless_com += [com_name] + duple
            return wrapped

        return decorator

    @classmethod
    def priority_list_created(cls, pr, elements):
        if len(cls.prior_com) <= pr:
            cls.prior_com += [] * (pr - len(cls.prior_com) + 1)
        cls.prior_com[pr] += (elements if type(elements) == list else [elements])
from vk.vk_commands import *
