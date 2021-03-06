# -*- coding: utf-8 -*-

from vk.vk_base_class import *


class VkListen(VkBase):
    from itertools import islice
    longpoll = None


    # =======! Starting !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), vip_users=dict(), **kw_cl):
        super().child_start(*ar_cl, queues=queues, vip_users=vip_users, **kw_cl)
        setattr(VkBotLongPoll, "changed_listen", changed_listen)
        cls.longpoll = VkBotLongPoll(cls.vk_session, group_id=cfg.get("vk", "group"))
        # print()
        cls.listen_events(queues, vip_users)

    # =======! Working !=======
    @classmethod
    def listen_events(cls, queues, vip_users, *ar_cl, **kw_cl):
        while cls.run:
            for ev in cls.longpoll.changed_listen(queues['finish_listen']):
                print('11')
                if ev == 'end':
                    print(12)
                    cls.run = False
                    print(13)
                    break
                # print(vip_users)
                # print(*[(i, d) for i, d in vip_users.items()], sep='\n')  # [(key, val) for key, val in d.items()]
                # print(*[[(key, val) for key, val in d.items()] for i, d in vip_users.items()], sep='\n')  #
                cls.processing_event(ev, queues, vip_users)
            print('--------------')


    # =======! Processing event !=======
    @classmethod
    def processing_event(cls, event, queues, vip_users):
        if hasattr(event, "type"):
            if event.type == VkBotEventType.MESSAGE_NEW:
                if not queues['listen'].empty():
                    cls.q_data_proc(queues['listen'].get())
                cls.processing_new_msg(event, queues, vip_users)
        else:
            print(cls.__name__, "пришло событие, которое не событие:", event)

    @classmethod
    def processing_new_msg(cls, event, queues, vip_users):
        # print('vip_users:', {key: {(k, v) for k, v in val.items()} for key, val in vip_users.items()})
        text = event.object.text
        # print(text)
        cl_com, text_find = (0, text) if len(text.split()) < 2 else (1, text.split()[0])
        print(event.raw)
        # если команда специальная, проверяем: ксть ли у пользователя соответствующий доступ
        if text_find in cls.admins_com and event.object.peer_id not in vip_users['admins']:
            cls.put_send('text', '''вы не админ, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /sign_in''', event.raw, queues=queues)
            return
        if text_find in cls.developers_com and event.object.peer_id not in vip_users['developers']:
            cls.put_send('text', '''вы не разработчик, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /dev_sign_in''', event.raw, queues=queues)
            return
        #
        # print('-===========')
        # проверяем, может команда не требует доступа к БД
        if text_find in cls.DBless_com[cl_com]:
            # print('---------------------')
            cls.func_for_com[text_find](cls, event=event.raw, queues=queues, vip_users=vip_users)
            return

        # если запрос нужно отправить сначала в обработку, то отправляем. В противном случае отправляем в БД
        for arr in [cls.prior_com_proc, cls.prior_com_db]:
            com, pr = next(cls.islice((((text_find if commands_p else None), ind)
                                       for ind, commands_p in enumerate(arr + [None])
                                       if not commands_p or text_find in commands_p[cl_com]), 1))
            # print('com, pr', com, pr)
            if com:  # com = None or list
                # print(cls.find_main_com, text_find)
                code_comand = cls.find_main_com[text_find]
                # print('*******')
                cls.func_for_com[code_comand](cls, code_comand, event=event.raw, pr=pr, queues=queues, vip_users=vip_users)
                return

        # если команда все еще не распознана, то проверяем,
        # может быть пришедший текст подходит под какую-нибудь функцию обработки
        func, (name_com, func_proc) = next(((key_f, val) for key_f, val in list(cls.rec_com.items()) + [
            (lambda i: True, (None, None))] if key_f(text)))
        if name_com:
            # print(vip_users)
            func_proc(cls, name_com, event=event.raw, queues=queues, vip_users=vip_users)
            return

        # если команда не распознана, то отправляем текста сообщения для составления цепей Маркова
        cls.put_proc('content', "/new_msg", (text, event.object.peer_id), pr=-1, queues=queues)

def changed_listen(self, end_queue):
    """ Слушать сервер

    :yields: :class:`Event`
    """
    from itertools import chain
    live = True
    end_iter = iter([])
    while live:
        # print('111')
        if not end_queue.empty():
            print('111')
            element = end_queue.get()
            print('112')
            if element == 'end':
                print('113')
                yield element
                print('114')
                return
            print(115)
            end_iter = chain(element, end_iter)
            print(116)
        for event in chain(end_iter, self.check()):
            # print(117)
            yield event
            # print(118)
            if event == 'end':
                return
        # print('----|||||||||||||||')



if __name__ == '__main__':
    from os import getcwd, chdir
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    chdir(path)