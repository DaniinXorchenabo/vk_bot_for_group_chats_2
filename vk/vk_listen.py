from vk.vk_base_class import *


class VkListen(VkBase):
    from itertools import islice
    longpoll = None

    # =======! Starting !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), vip_users=dict(), **kw_cl):
        super().child_start(*ar_cl, queues=queues, vip_users=vip_users, **kw_cl)
        cls.longpoll = VkBotLongPoll(cls.vk_session, group_id=cfg.get("vk", "group"))
        cls.listen_events(queues, vip_users)

    # =======! Working !=======
    @classmethod
    def listen_events(cls, queues, vip_users, *ar_cl, **kw_cl):
        while cls.run:
            for ev in cls.longpoll.listen():
                cls.processing_event(ev, queues, vip_users)

    # =======! Processing event !=======
    @classmethod
    def processing_event(cls, event, queues, vip_users):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not queues['listen'].empty():
                cls.q_data_proc(queues['listen'].get())
            cls.processing_new_msg(event, queues, vip_users)

    @classmethod
    def processing_new_msg(cls, event, queues, vip_users):

        text = event.object.text
        print(text)
        cl_com, text_find = (0, text) if len(text.split()) < 2 else (1, text.split()[0])

        # если команда специальная, проверяем: ксть ли у пользователя соответствующий доступ
        if text_find in cls.admin_com and not cls.admins.get(event.object.peer_id, None):
            cls.put_send('text', '''вы не админ, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /login''', event.raw, queues=queues)
            return
        if text_find in cls.developer_com and not cls.developers.get(event.object.peer_id, None):
            cls.put_send('text', '''вы не разработчик, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /login_dev''', event.raw, queues=queues)
            return

        print('-===========')
        # проверяем, может команда не требует доступа к БД
        if text_find in cls.DBless_com[cl_com]:
            cls.func_for_com[text_find](cls, event=event.raw, queues=queues)
            return

        # если запрос нужно отправить сначала в обработку, то отправляем. В противном случае отправляем в БД
        for arr, q_func in [(cls.prior_com_proc, cls.put_proc),
                            (cls.prior_com_db, cls.put_db)]:
            com, pr = next(cls.islice(((commands_p, ind) for ind, commands_p in enumerate(arr + [None])
                                       if not commands_p or text_find in commands_p[cl_com]), 1))
            print('com, pr', com, pr)
            if com:  # com = None or list
                code_comand = cls.find_main_com[text_find](cls)
                cls.func_for_com[text_find](cls, code_comand, event.raw, pr=pr, queues=queues)
                return
        peer_id = event.object.peer_id
        cls.put_proc('content', "/new_msg", (text, peer_id), pr=-1, queues=queues)
        # отправление текста сообщения для составления цепей Маркова
