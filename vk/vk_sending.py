from vk.vk_base_class import *


class VkSending(VkBase):
    admin_pas = dev_pas = None  # пароли админа и разработчика
    obj_dict = dict()  # dict(id_chat: VkBotSending)

    # =======! Starting !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), vip_users=dict(), **kw_cl):
        super().child_start(*ar_cl, queues=queues, vip_users=vip_users, **kw_cl)
        cls.admin_pas = cfg.get("passwords", "admin")
        cls.dev_pas = cfg.get("passwords", "developer")
        cls.working(queues, vip_users, *ar_cl, **kw_cl)

    # =======! Working !=======
    @classmethod
    def working(cls, queues, users, *ar_cl, **kw_cl):
        while cls.run:
            if not queues['send'].empty():
                cls.q_data_proc(*queues['send'].get())
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
    def text_type_proc(cls, text, last_msg, *args, queues=dict(), **kwargs):
        cls.gen_and_send_msg(text, last_msg)

    # =======! Processing !=======
    @classmethod
    def add_peculiar_properties(cls, old_msg):
        if old_msg.get('peer_id', None) and cls.obj_dict.get(old_msg.get('peer_id')):
            # характеристики сообщений чата, присущие только ему (к примеру, клавиатура)
            old_msg.update(cls.obj_dict[old_msg['peer_id']].own_dict)
        return old_msg

    # =======! Sending !=======
    @classmethod
    def gen_and_send_msg(cls, text, old_msg):
        cls.send_msg(cls.gen_msg(text, old_msg))

    @classmethod
    def send_msg(cls, msg: dict):
        cls.vk_session.method("messages.send", cls.add_peculiar_properties(msg))


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
