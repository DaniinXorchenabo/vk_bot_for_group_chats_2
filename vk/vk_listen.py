from vk.vk_base_class import *


class VkListen(VkBase):
    from itertools import islice
    longpoll = None

    # =======! Starting !=======
    @classmethod
    def child_start(cls, queues, vip_users, *ar_cl, **kw_cl):
        super().child_start(queues, vip_users, *ar_cl, **kw_cl)
        cls.longpoll = VkBotLongPoll(cls.vk_session, group_id=cfg.get("vk", "group"))
        cls.listen_events()

    # =======! Working !=======
    @classmethod
    def listen_events(cls, queues, vip_users, *ar_cl, **kw_cl):
        while cls.run:
            for ev in cls.longpoll.listen():
                cls.checking_q(queues)
                cls.processing_event(ev, queues, vip_users)

    @classmethod
    def checking_q(cls, queues):
        pass

    # =======! Processing event !=======
    @classmethod
    def processing_event(cls, event, queues, vip_users):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not queues['listen'].empty():
                cls.q_data_proc(queues['listen'].get())
            cls.processing_new_msg(event, queues, vip_users)

    @classmethod
    def processing_new_msg(cls, event, queues, vip_users):
        # сначала проверяем, вдруг запрос не требует доступа к БД (сначала сообщения без аргументов, мотом с ними)
        text = event.object.text
        cl_com, text_find = (0, text) if len(text.split()) < 2 else (1, text.split()[0])
        if text_find in cls.admin_com and not cls.admins.get(event.object.peer_id, None):
            cls.put_send('text', '''вы не админ, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /login''', event.raw, queues=queues)
            return
        if text_find in cls.developer_com and not cls.developers.get(event.object.peer_id, None):
            cls.put_send('text', '''вы не разработчик, поэтому не можете использовать данную команду.
             Если это не так, то попробуйте ввести: /login_dev''', event.raw, queues=queues)
            return
        if text_find in cls.DBless_com[cl_com]:
            cls.put_send('func', cls.func_for_com[text_find], [], {'queues': queues, 'event': event.raw}, queues=queues)
            return
        com, pr = next(cls.islice(((commands_p, ind) for ind, commands_p in enumerate(cls.prior_com + [None])
                                   if not commands_p or text_find in commands_p[cl_com]), 1))
        if com:  # com = None or list
            cls.put_proc('ev', cls.find_main_com[text_find], event.raw, cls.func_for_com[text_find], [], {}, pr=pr, queues=queues)
            return
        cls.put_proc('ev', "/new_msg", event.raw, cls.func_for_com[text_find], [], {}, pr=-1, queues=queues)
        # отправление текста сообщения для составления цепей Маркова


