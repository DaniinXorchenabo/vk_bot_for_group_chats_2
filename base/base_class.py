from base.base_libs import *

class BaseClass:
    from pymorphy2 import MorphAnalyzer
    from nltk import word_tokenize as nltk_w_tok
    # nltk.download('punkt')

    run = False
    kw = dict()
    funk_kw = dict()
    list_keys = ['user_id', "random_id", "peer_id", "domain",
                 "chat_id", "user_ids", "message", "lat", "long",
                 "attachment", "reply_to", "forward_messages",
                 "sticker_id", "group_id", "keyboard", "payload",
                 "dont_parse_links", "disable_mentions", "intent",
                 "subscribe_id"]
    prob_thresh = 0.4
    morph = None

    # =======! Инициализация !=======
    @classmethod
    def common_start(cls, queues=dict(), types=[]):
        cls.create_relation_proc(queues)
        cls.gen_proc_func_from_types(types)
        cls.morph = cls.MorphAnalyzer()

    @classmethod
    def start(cls, *ar_cl, queues=dict(), types=[], **kw_cl):
        try:
            cls.create_relation_proc(queues)
            cls.gen_proc_func_from_types(types)
            cls.run = True
            print('child_start starting ')
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

        print('создание очередей без приоритета:', end='\t')
        [(setattr(BaseClass, 'put_' + key,
                 staticmethod(lambda _type, *content, queues=dict(), key_f=str(key): (print('put_' + key_f + ' working ---=-=-=-=', queues[key_f]), queues[key_f].put((_type, content)), print('put_' + key_f + ' ended', end='\t')))),
          print('put_' + key, end='\t'))
         for key, q in queues.items() if type(q) != list and not hasattr(BaseClass, 'put_' + key)]
        print('завершилось')

        print('создание очередей с приоритетом:', end='\t')
        [(setattr(BaseClass, 'put_' + key,
                 staticmethod(lambda _type, *content, pr=-1, queues=dict(), key_f=str(key): queues[key_f][pr].put((_type, content)))), print('put_' + key, end='\t'))
         for key, q in queues.items() if type(q) == list and not hasattr(BaseClass, 'put_' + key)]  # pr - приоритет
        print('завершилось')

        print(cls.__name__, 'создание получения элемента с приоритетом....', end='\t')
        [setattr(BaseClass, 'get_' + key, staticmethod(
            lambda queues=dict(), key_f=str(key): next(map(lambda i: (i if not i else i.get()), islice(
                dropwhile(lambda i: (hasattr(i, 'empty') and i.empty()), iter(queues[key_f] + [None])), 1)))))
         for key, q in queues.items() if type(q) == list and not hasattr(BaseClass, 'get_' + key)]
        print('успешно завершено')

    @classmethod
    def q_data_proc(cls, _type, content, *ar_cl, queues=dict(), **kw_cl):
        print(hasattr(cls, _type + '_type_proc'))
        if hasattr(cls, _type + '_type_proc'):
            print(getattr(cls, _type + '_type_proc'), content)
            getattr(cls, _type + '_type_proc')(*content, queues=queues, **kw_cl)

    @classmethod
    def gen_proc_func_from_types(cls, types):
        [setattr(cls, str(name_type) + '_type_proc', classmethod(lambda cls, *args, queues=dict(), **kwargs: None))
         for name_type in types if not hasattr(cls, str(name_type) + '_type_proc')]


    # =======! Создание ответа !=======
    @classmethod
    def gen_msg(cls, text: str, old_msg: dict):
        print('90080980*&&&&&&&&&&&&&&&&&&&&&')
        aaa = cls.correcting_msg_text(text)
        print(aaa)
        return cls.gen_answ_dict(old_msg, aaa, func=lambda i: type(i) != dict)

    @classmethod
    def correcting_msg_text(cls, text):
        if not cls.morph:
            cls.morph = cls.MorphAnalyzer()
        print('correcting_msg_text')
        if type(text) != list:
            if type(text) == str:
                text = cls.nltk_w_tok(text)
            elif type(text) == dict:
                text = text.keys()
            else:
                text = list(text)
        print('correcting_msg_text ...')
        return re_sub(r'(\s{1,})([.,!:;])', r'\2', ' '.join([(word.title() if bool(list(
            filter(lambda p: p.score > cls.prob_thresh and ('Name' in p.tag or 'Sgtm' in p.tag or "Geox" in p.tag),
                   cls.morph.parse(word)))) or ind == 0 else word) for ind, word in enumerate(text)]))

    @classmethod
    def gen_answ_dict(cls, _dict: dict, text: str, func=lambda i: True, deep=0):
        print('gen_answ_dict started')
        if deep > 2:
            return dict()
        nested_dict = []
        standart_d = {key: val for key, val in _dict.items()
                      if not (type(val) == dict and nested_dict.append(key)) and key in cls.list_keys and func(val)}
        [standart_d.update(cls.gen_answ_dict(_dict[key], '', deep=deep + 1, func=func)) for key in nested_dict]
        if deep == 0:
            standart_d.update({"message": text, 'random_id': randint(1, 2147483647)})
            print('gen_answ_dict ended')
        return standart_d




    # # =======! Testing !=======
    # @classmethod
    # def base_proc(cls, msg):
    #     for i in cls.kw:
    #         if msg == i:
    #             cls.kw[i]()
    #
    # @classmethod
    # def test(cls, base_com, list_comands: list = [], func_com: list = []):
    #     def decorator(func):
    #         def decorator_decorator(*args2, **kwargs2):
    #             print('************')
    #             func(*args2, **kwargs2)
    #             print('************')
    #
    #         cls.kw.update({i: decorator_decorator for i in [base_com] + list_comands})
    #         cls.funk_kw.update({i: decorator_decorator for i in func_com})
    #         return decorator_decorator
    #
    #     return decorator


# @BaseClass.test('привет')
# def proc_1_2(*ar, **kw):
#     print('и тебе привет!')
#
#
# @BaseClass.test('пока')
# def proc_1_5(*ar, **kw):
#     print('и тебе пока!')
#     print('arrrrrrrrrrrrrrrrrrrrrrrr')



# setattr(BaseClass, 'printer', classmethod(lambda i, word='хей хей хей': print(word)))
# BaseClass.printer()  # >>хей хей хе

if __name__ == '__main__':
    from os import getcwd, chdir
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)