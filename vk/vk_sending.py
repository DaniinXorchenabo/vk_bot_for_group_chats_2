from vk.vk_base_class import *


class VkSending(VkBase):
    from pymorphy2 import MorphAnalyzer
    from nltk import word_tokenize as nltk_w_tok
    # nltk.download('punkt')

    prob_thresh = 0.4
    morph = None
    admin_pas = dev_pas = None  # пароли админа и разработчика
    obj_dict = dict()  # dict(id_chat: VkBotSending)

    # =======! Starting !=======
    @classmethod
    def child_start(cls, *ar_cl, queues=dict(), vip_users=dict(), **kw_cl):
        super().child_start(*ar_cl, queues=queues, vip_users=vip_users, **kw_cl)
        cls.admin_pas = cfg.get("passwords", "admin")
        cls.dev_pas = cfg.get("passwords", "developer")
        cls.morph = cls.MorphAnalyzer()
        cls.working(queues, vip_users, *ar_cl, **kw_cl)

    # =======! Working !=======
    @classmethod
    def working(cls, queues, users, *ar_cl, **kw_cl):
        while cls.run:
            if not queues['send'].empty():
                cls.send_msg(*cls.q_data_proc(*queues['send'].get()))
            else:
                sleep(0.1)

    # =======! Processing !=======
    @classmethod
    def gen_answ_dict(cls, _dict: dict, func=lambda i: True, deep=0):
        if deep > 2:
            return dict()
        nested_dict = []
        standart_d = {key: val for key, val in _dict.items()
                      if not (type(val) == dict and nested_dict.append(key)) and key in cls.list_keys and func(val)}
        [standart_d.update(cls.gen_answ_dict(_dict[key]), deep=deep + 1, func=func) for key in nested_dict]
        return standart_d

    @classmethod
    def constructor_msg(cls, text, old_msg):
        return cls.correcting_msg_dict(cls.correcting_msg_text(text), old_msg)

    @classmethod
    def correcting_msg_text(cls, text):
        if type(text) != list:
            if type(text) == str:
                text = cls.nltk_w_tok(text)
            elif type(text) == dict:
                text = text.keys()
            else:
                text = list(text)
        return re_sub(r'(\s{1,})([.,!:;])', r'\2', ' '.join([(word.title() if bool(list(
            filter(lambda p: p.score > cls.prob_thresh and ('Name' in p.tag or 'Sgtm' in p.tag or "Geox" in p.tag),
                   cls.morph.parse(word)))) or ind == 0 else word) for ind, word in enumerate(text)]))

    @classmethod
    def correcting_msg_dict(cls, text, old_msg):
        if old_msg.get('peer_id', None) and cls.obj_dict.get(old_msg.get('peer_id')):
            # характеристики сообщений чата, присущие только ему (к примеру, клавиатура)
            old_msg.update(cls.obj_dict[old_msg['peer_id']].own_dict)
        old_msg.update({"message": text, 'random_id': randint(1, 2147483647)})
        return old_msg

    # =======! Sending !=======
    @classmethod
    def send_msg(cls, text, old_msg):
        msg = cls.gen_answ_dict(cls.constructor_msg(text, old_msg), func=lambda i: type(i) != dict)
        cls.vk_session.method("messages.send", msg)



if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)