from vk.vk_base_class import VkBase
from vk.vk_buttons import *
from random import randint


@VkBase.commands('/help', duple=['помощь', "помоги", "/h"])
def get_text_help_comand(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    if not bool(cls.help_command):
        with open('settings/commands.txt', 'r', encoding='utf-8') as f:
            cls.help_command = f.read()
    cls.put_send('text', cls.help_command, event, queues=queues)


@VkBase.commands('/gen', db_acc=(-2, True))
def gen_random_text(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/gen', event, queues=queues, pr=-2)


@VkBase.commands('/erease', duple=['/er', "очистить_память_чата", "очистить_память_беседы"], db_acc=(False, 0))
def gen_random_comand(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/erease', event, queues=queues, pr=0)


@VkBase.commands('/stat', duple=['получить_статистику', '/st'], db_acc=(False, 0))
def gen_stat_for_chat(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    cls.put_db('content', '/stat', event, queues=queues, pr=0)


@VkBase.commands('/get_ans_from_bot', rec_f=[lambda text: text[:4].lower() == 'бот,' and text[-1] == '?'])
def get_answer_for_your_question(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    ANSWERS = ['Да', 'Нет', 'Не знаю', 'Сложно ответить',
               'Даже мудрецы не знают ответа на этот вопрос',
               'Не важно. Съешь яблоко!', 'А почему ты спрашиваешь?',
               'Скорее нет, чем да', 'Скорее да, чем нет',
               'Что?', 'Ты пятый раз это спрашиваешь!']
    ans = ANSWERS[randint(0, len(ANSWERS) - 1)]
    cls.put_send('text', ans, event, queues=queues)


@VkBase.commands('/set_keyword', duple=['Установить клавиатуру', '/kw', "/keyword"], db_acc=False)
def set_standart_kw(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    id_chat = event['object']['peer_id']

    cls.put_send('change_param', id_chat, "Клавиатура установлена", {"keyboard": standart_kw_cl.get_dict()},
                 queues=queues)
    # print(standart_kw_cl.get_dict())


@VkBase.commands('/del_keyword', duple=['Убрать клавиатуру', '/n_kw', "/no_keyword"], db_acc=False)
def set_standart_kw(cls, *ar_f, event=dict(), queues=dict(), **kw_f):
    id_chat = event['object']['peer_id']
    cls.put_send('change_param', id_chat, "Клавиатура убрана", {"keyboard": del_keyboard.get_dict()}, queues=queues)
    # print(standart_kw_cl.get_dict())


@VkBase.commands('/log_in', it_is_part=1, db_acc=(False, 0))
def admin_log_in(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(),
                 ans1='нельзя войти в админку, если вы уже в админке)',
                 ans2='Вы уже администратор, чтобы использовать все команды, доступные вам, введите "/sign_in"',
                 ans3='Поздравляю! Теперь вы администратор!',
                 who='admin', password=None, **kw_f):
    if not password:
        password = cls.admin_pas
    all_text = (event['object']['text'].split() + [''])[1]
    peer_id = event['object']['peer_id']
    print(*[[(key, val) for key, val in s.items()] for d, s in vip_users.items()])
    if peer_id in vip_users[f'{who}s']:
        ans = ans1 if vip_users[f'{who}s'][peer_id] else ans2
        cls.put_send('text', ans, event, queues=queues)
        return
    # print(f'{who}_pas', getattr(cls, f'{who}_pas'))
    if all_text == password:
        vip_users[f'{who}s'][peer_id] = True
        cls.put_db('content', f'/add_{who}', {}, peer_id, queues=queues, pr=0)
        cls.put_send('text', ans3, event, queues=queues)
    else:
        if bool(all_text):
            ans = 'Неправильный пароль'
            cls.put_send('text', ans, event, queues=queues)


@VkBase.commands('/dev_log_in', it_is_part=1, db_acc=(False, 0))
def developer_log_in(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    admin_log_in(cls, *ar_f, event=event, queues=queues, vip_users=vip_users,
                 ans1='нельзя стать разработчиком если вы уже разработчик)',
                 ans2='Вы уже разработчик, чтобы использовать все команды, доступные вам, введите "/dev_sign_in"',
                 ans3='Поздравляю! Теперь вы разработчик!',
                 who='developer', password=cls.developer_pas, **kw_f)


@VkBase.commands('/sign_in', adm_com=True)  #
def sign_in_admin(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), who='admin', who2='администратор', **kw_f):
    peer_id = event['object']['peer_id']
    if peer_id in vip_users[f'{who}s']:
        if vip_users[f'{who}s'].get(peer_id):
            ans = 'Вы уже ' + who + ", вам уже доступны команды " + who2 + 'а'
        else:
            vip_users[f'{who}s'][peer_id] = True
            ans = 'Вы вошли как ' + who + ', теперь вам доступны команды ' + who2 + 'а'
        cls.put_send('text', ans, event, queues=queues)


@VkBase.commands('/dev_sign_in', dev_com=True)
def sign_in_developer(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    sign_in_admin(cls, *ar_f, event=event, queues=queues, vip_users=vip_users, who='developer', who2='разработчик', **kw_f)


@VkBase.commands('/sign_out', adm_com=True)
def sign_out_admin(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), who='admin', who2='администратор', **kw_f):
    peer_id = event['object']['peer_id']
    if peer_id in vip_users[f'{who}s']:
        if vip_users[f'{who}s'].get(peer_id):
            ans = 'Вы вышли из сессии ' + who2 + 'а'
            vip_users[f'{who}s'][peer_id] = False
        else:
            ans = 'нельзя выйти из сессии ' + who2 + 'а, если вы еще не ' + who2 + ')))'
        cls.put_send('text', ans, event, queues=queues)


@VkBase.commands('/dev_sign_out', dev_com=True)
def sign_out_developer(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    sign_out_admin(cls, *ar_f, event=event, queues=queues, vip_users=vip_users, who='developer', who2='разработчик', **kw_f)


@VkBase.commands('/stat_me')
def get_users_info(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    peer_id = event['object']['peer_id']
    ans = ''
    for name, _dict in vip_users.items():
        if peer_id in _dict:
            ans += 'вы - ' + name + '\n'
            ans += ('вы находитесь в сессии' if _dict[peer_id] else
                    'но сейчас вым доступны только команды обычного пользователя') + '\n'
    if not bool(ans):
        ans += 'вы обладаете правами обычного пользователя'
    cls.put_send('text', ans, event, queues=queues)


@VkBase.commands('/del_me', db_acc=(False, 0), adm_com=True)
def del_me_for_admin(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    peer_id = event['object']['peer_id']
    if peer_id in vip_users[f'admins']:
        del vip_users['admins'][peer_id]
        cls.put_db('content', '/del_me', event, peer_id, pr=0, queues=queues)


@VkBase.commands('/dev_del_me', db_acc=(False, 0), dev_com=True)
def del_me_for_developer(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    peer_id = event['object']['peer_id']
    if peer_id in vip_users[f'developers']:
        del vip_users['developers'][peer_id]
        cls.put_db('content', '/dev_del_me', event, peer_id, pr=0, queues=queues)


@VkBase.commands('/add_admin', db_acc=(False, 0), adm_com=True, dev_com=True, it_is_part=1)
def add_new_admin(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), who='admin', who2='админ', who3='', **kw_f):
    all_text = (event['object']['text'].split() + [''])[1]
    peer_id = event['object']['peer_id']
    if not all_text.isdigit():
        ans = f'после /add_{who} должно идти id, только из цифр'
        cls.put_send('text', ans, event, queues=queues)
        return
    new_adm = int(all_text)
    if new_adm in vip_users[who + 's']:
        ans = f'нельзя назначить {who2}ом человека, который уже {who2}))))'
        cls.put_send('text', ans, event, queues=queues)
        return
    cls.put_db('content', f'/add_{who}', {}, new_adm, pr=0, queues=queues)
    vip_users[who + 's'][new_adm] = False
    ans = f'пользователь назначен {who2}ом, чтобы войти в сессию, ему необходимо ввести: /{who3}sign_in'
    cls.put_send('text', ans, event, queues=queues)
    print(*[[(key, val) for key, val in s.items()] for d, s in vip_users.items()])


@VkBase.commands('/add_developer', db_acc=(False, 0), dev_com=True, it_is_part=1)
def add_new_developers(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), **kw_f):
    add_new_admin(cls, *ar_f, event=event, queues=queues, vip_users=vip_users,
                       who='developer', who2='разработчик', who3='dev_', **kw_f)


@VkBase.commands('/del_admin', db_acc=(False, 0), dev_com=True, it_is_part=1)
def del_admin(cls, *ar_f, event=dict(), queues=dict(), vip_users=dict(), who='admin', who2='админ', who3='', **kw_f):
    all_text = (event['object']['text'].split() + [''])[1]
    peer_id = event['object']['peer_id']
    if not all_text.isdigit():
        ans = f'после /del_admin должно идти id, только из цифр'
        cls.put_send('text', ans, event, queues=queues)
        return
    del_adm = int(all_text)
    if del_adm not in vip_users['admins']:
        ans = f'нельзя удалить человека из состава администраторов, если он на администратор'
        cls.put_send('text', ans, event, queues=queues)
        return
    del vip_users['admins'][del_adm]
    cls.put_db('content', '/del_me', event, del_adm, pr=0, queues=queues)
    ans = f'пользователь был удалён из состава администраторов'
    cls.put_send('text', ans, event, queues=queues)
    print(*[[(key, val) for key, val in s.items()] for d, s in vip_users.items()])


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
