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
                cls.q_data_proc(*q_or_none.get(), queues=queues)  # -> cls.event_type_proc()

    # =======! Processing !=======
    @classmethod
    def event_type_proc(cls, type_ev: str, data: dict, func, args_for_func, kwargs_for_func, *ar_cl, queues=dict(), **kw_cl):
        cls.func_for_com[type_ev](type_ev, data, func, args_for_func, kwargs_for_func, queues=queues)

    # =======! добавление функций обработки в список !=======
    @classmethod
    def command(cls, com_name, pr=-1):
        def decorator(func):
            def wrapped(_type, *args_dec, queues=dict(), **kwargs_dec):
                res = func(cls, *args_dec, **kwargs_dec)
                cls.put_db(_type, *res, pr=pr, queues=queues)
                return res

            cls.func_for_com[com_name] = wrapped
            return wrapped

        return decorator

    @classmethod
    def edit_msd_text(cls, text):
        if type(text) == list:
            text = ' '.join(text)
        _dict = dict()
        start_w_dict = dict()
        for part in (part.split() for part in
                     iter(re_sub(r'()([.!?\n]{1,})',
                                 r'\1 \2 #@*`~', re_sub(r'([^.,!:;? ])()([.,!:?;\n]{1,})', r'\1 \2 \3',
                                                        re_sub(r'''[«»{}\][()"'*#$^~`]''', '', text.lower()))).split(
                         '#@*`~'))
                     if len(part.split()) > 0):
            if len(part) == 1:
                part += ['.']
            for i in range(1, len(part) - 1):
                _dict[part[i]] = _dict.get(part[i], cls.Counter()) + cls.Counter({part[i + 1]: 1})
            start_w_dict[part[0]] = start_w_dict.get(part[0], cls.Counter()) + cls.Counter({part[1]: 1})
            _dict[part[-1]] = start_w_dict.get(part[-1], cls.Counter())
        return [start_w_dict, _dict]


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)