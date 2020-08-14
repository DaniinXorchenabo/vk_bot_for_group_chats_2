from base.base_class import BaseClass
from db.models import *
from base.base_libs import *

class ControlDB(BaseClass):
    func_for_com = dict()

    # =======! Started !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), **kw_cl):
        cls.working(*ar_cl, queues=queues, **kw_cl)

    # =======! Working !=======
    @classmethod
    def working(cls, *ar_cl, queues=dict(), **kw_cl):
        while cls.run:
            queue = cls.get_db(queues=queues)
            if queue:
                cls.q_data_proc(queue.get())
            else:
                sleep(0.1)

    # =======! Processing !=======
    @classmethod
    def content_type_proc(cls, comamnd, *args_q,  queues=dict(), **kwargs_q):
        cls.func_for_com[comamnd](comamnd, *args_q, queues=queues, **kwargs_q)

    @classmethod
    def event_type_proc(cls, type_ev: str, data: dict, func, args_f, kwargs_f, *ar_cl, queues=dict(), **kw_cl):
        cls.func_for_com[type_ev](type_ev, data, func, args_f, kwargs_f, *ar_cl, queues=queues, **kw_cl)

    # =======! Create Decorator !=======
    @classmethod
    def command(cls, comand):
        def decorator(func):
            def wrapped(*args, **kwargs):
                return func(cls, *args, **kwargs)
            cls.func_for_com[comand] = wrapped
            return wrapped
        return decorator





if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)

from db.db_controller_func import *