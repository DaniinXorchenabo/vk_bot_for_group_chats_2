# -*- coding: utf-8 -*-

from vk.vk_base_class import *


class VkSending(VkBase):
    obj_dict = dict()  # dict(id_chat: VkBotSending)

    # =======! Starting !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), vip_users=dict(), **kw_cl):
        super().child_start(*ar_cl, queues=queues, vip_users=vip_users, **kw_cl)
        cls.working(queues, vip_users, *ar_cl, **kw_cl)

    # =======! Working !=======
    @classmethod
    def working(cls, queues, vip_users, *ar_cl, **kw_cl):
        while cls.run:
            if not queues['send'].empty():
                # print('-----------------------')
                cls.q_data_proc(*queues['send'].get(), vip_users=vip_users, queues=queues)
                # if data and bool(data):
                #     if type(data) == list and len(data) == 2:
                #         cls.gen_and_send_msg(*data)
                #         continue
                #     elif type(data) == dict:
                #         cls.send_msg(data)
                #         continue
            else:
                sleep(0.1)

    # =======! Обработка Очередей !=======
    @classmethod
    def cooking_msg_type_proc(cls, msg_dict, *args, queues=dict(), **kwargs):
        cls.send_msg(msg_dict)

    @classmethod
    def text_type_proc(cls, text: str, last_msg: dict, *args, queues=dict(), **kwargs):
        cls.gen_and_send_msg(text, last_msg)

    @classmethod
    def change_param_type_proc(cls, peer_id: int, text: str, data: dict, queues=dict(), **kwargs):
        # print('----')
        if not cls.obj_dict.get(peer_id):
            cls(peer_id)
        cls.obj_dict[peer_id].__dict__.update(data)
        cls.gen_and_send_msg(text, {'peer_id': peer_id})
        # print('-00((((((((')

    @classmethod
    def inner_info_type_proc(cls, _type, data, queues=dict(), vip_users=dict(), **kwargs):
        # print('03333333333333322222222222222-------------------------------')
        if _type == 'set_admins':
            vip_users['admins'].update({i: False for i in data})
        elif _type == 'set_developers':
            vip_users['developers'].update({i: False for i in data})

    # =======! Processing !=======
    @classmethod
    def add_peculiar_properties(cls, old_msg):
        print('add_peculiar_properties working!')
        if old_msg.get('peer_id') and not cls.obj_dict.get(old_msg.get('peer_id')):
            cls(old_msg['peer_id'])
        if old_msg.get('peer_id'):
            # характеристики сообщений чата, присущие только ему (к примеру, клавиатура)
            old_msg.update(cls.obj_dict[old_msg['peer_id']].__dict__)
        print('add_peculiar_properties end working!')
        return old_msg

    # =======! Sending !=======
    @classmethod
    def gen_and_send_msg(cls, text: str, old_msg: dict):
        print('gen_and_send_msg working!', text, old_msg)
        cls.send_msg(cls.gen_msg(text, old_msg))

    @classmethod
    def send_msg(cls, msg: dict):
        print('send_msg working!')
        aaa = cls.add_peculiar_properties(msg)
        print(aaa)
        cls.vk_session.method("messages.send", aaa)

    # =======! Работа с объектом чата !=======
    def __init__(self, chat_id, kw=None):
        if not VkSending.obj_dict.get(chat_id):
            VkSending.obj_dict[chat_id] = self
        self.peer_id = chat_id
        self.keyboard = kw


if __name__ == '__main__':
    from os import getcwd, chdir
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    chdir(path)
