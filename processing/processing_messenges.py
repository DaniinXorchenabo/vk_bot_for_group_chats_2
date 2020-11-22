# -*- coding: utf-8 -*-

from base.base_class import *


class ProcessingMsg(BaseClass):
    from collections import Counter

    func_for_com = dict()  # {'command_name': working_finc, ...}

    # =======! Starting !=======
    @classmethod
    def child_start(cls, queues, *ar_cl, **kw_cl):
        cls.working(queues)

    # =======! Working !=======
    @classmethod
    def working(cls, queues):
        while cls.run:
            q_or_none = cls.get_proc(queues=queues)

            if q_or_none:
                # print('from ProcessingMsg.working', q_or_none)
                cls.q_data_proc(*q_or_none, queues=queues)  # -> cls.event_type_proc() or content_type_proc()
            else:
                sleep(0.1)

    # =======! Processing !=======
    @classmethod
    def event_type_proc(cls, type_ev, *args, queues=dict(),
                        **kw_cl):  # str, data: dict, func, args_for_func, kwargs_for_func, *ar_cl, queues=dict(),
        cls.func_for_com[type_ev](cls, type_ev, *args, queues=queues, **kw_cl)

    @classmethod
    def content_type_proc(cls, type_ev, data, *args, queues=dict(), **kw_cl):
        # print(type_ev, *data)

        cls.func_for_com[type_ev](cls, type_ev, *data, queues=queues, **kw_cl)

    # =======! добавление функций обработки в список !=======
    @classmethod
    def command(cls, com_name, pr=-1):
        def decorator(func):
            def wrapped(_type, data: dict, func_vk, args_vk, kwargs_vk, *args_dec, queues=dict(), **kwargs_dec):
                """

                :param _type: нужен для дальнейшей отправки в БД
                :param data: словарь с событием
                :param func_vk: функция обработки сообщения для вк
                :param args_vk: аргументы для func_vk
                :param kwargs_vk: именованные аргументы для func_vk
                :param args_dec:
                :param queues: нужны для отправки в БД
                :param kwargs_dec:
                :return:
                """
                res = func(cls, *args_dec, **kwargs_dec)  # функция должна класть результаты в очередь
                # cls.put_db(_type, *res, pr=pr, queues=queues)
                return res

            cls.func_for_com[com_name] = func
            return wrapped

        return decorator


if __name__ == '__main__':
    from os import getcwd, chdir
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    chdir(path)

from processing.processing_func import *
