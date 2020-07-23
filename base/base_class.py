from base.base_libs import *

class BaseClass:
    run = False
    kw = dict()
    funk_kw = dict()

    # =======! Инициализация !=======
    @classmethod
    def start(cls, *ar_cl, queues=dict(), **kw_cl):
        try:
            cls.create_relation_proc(queues)
            cls.run = True
            cls.child_start(*ar_cl, queues=queues, **kw_cl)
        except Exception as e:
            print('произошла ошибка в', cls.__name__ + ':', e)
        cls.run = False
        return cls.start

    @classmethod
    def child_start(cls, *ar_cl, **kw_cl):
        pass

    # =======! связь между процессами !=======
    @classmethod
    def create_relation_proc(cls, queues):
        from itertools import dropwhile, islice

        [setattr(BaseClass, 'put_' + key,
                 staticmethod(lambda _type, *content, queues=dict(): queues[key].put((_type, content))))
         for key, q in queues.items() if type(q) != dict and not hasattr(BaseClass, 'put_' + key)]
        [setattr(BaseClass, 'put_' + key,
                 staticmethod(lambda _type, *content, pr=-1, queues=dict(): queues[key][pr].put((_type, content))))
         for key, q in queues.items() if type(q) == dict and not hasattr(BaseClass, 'put_' + key)]  # pr - приоритет
        [setattr(BaseClass, 'get_' + key,
                 staticmethod(lambda queues=dict(): next(map(lambda i: (i if i else i.get()), (islice(
                     dropwhile(lambda i: not i or i.empty(), iter(queues[key] + [None])), 1)))))  )
         for key, q in queues.items() if type(q) == dict and not hasattr(BaseClass, 'get_' + key)]

    @classmethod
    def q_data_proc(cls, _type, content, *ar_cl, **kw_cl):
        if _type == 'func':
            func, ar_finc, kw_func = content
            return func(*ar_finc, **kw_func)
        elif _type == 'ev':
            cls.event_type_proc(*content, *ar_cl, **kw_cl)
        elif _type == 'text':
            return content

    @classmethod
    def event_type_proc(cls, type_ev: str, data: dict, func, args, kwargs, *ar_cl, **kw_cl):
        pass

    # =======! Testing !=======
    @classmethod
    def base_proc(cls, msg):
        for i in cls.kw:
            if msg == i:
                cls.kw[i]()

    @classmethod
    def test(cls, base_com, list_comands: list = [], func_com: list = []):
        def decorator(func):
            def decorator_decorator(*args2, **kwargs2):
                print('************')
                func(*args2, **kwargs2)
                print('************')

            cls.kw.update({i: decorator_decorator for i in [base_com] + list_comands})
            cls.funk_kw.update({i: decorator_decorator for i in func_com})
            return decorator_decorator

        return decorator


@BaseClass.test('привет')
def proc_1_2(*ar, **kw):
    print('и тебе привет!')


@BaseClass.test('пока')
def proc_1_5(*ar, **kw):
    print('и тебе пока!')
    print('arrrrrrrrrrrrrrrrrrrrrrrr')


class Child(BaseClass):
    pass


class BaseClass: pass


setattr(BaseClass, 'printer', classmethod(lambda i, word='хей хей хей': print(word)))
BaseClass.printer()  # >>хей хей хе

if __name__ == '__main__':
    from os import getcwd, chdir
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)

    Child.base_proc('пока')
