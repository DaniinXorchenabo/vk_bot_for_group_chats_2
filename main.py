def error_callback_func(*args, **kwargs):
    print('---------------------------------')
    print('error_callback_func', )
    print(args)
    print(kwargs)
    print('---------------------------------')


if __name__ == '__main__':
    from base.base_libs import *
    from base.base_class import BaseClass
    from vk.vk_base_class import VkBase
    # from vk.vk_commands import *
    from processing.processing_messenges import ProcessingMsg
    from db.db_controller import ControlDB
    from vk.vk_listen import VkListen
    from vk.vk_sending import VkSending
    print('-0-0-0-0-0-0-0')
    from multiprocessing import Pool, cpu_count, Manager
    print('-0-0-0-0-0-0-0')


    # =======! initialization !=======
    pool = Pool(processes=2)
    print('=0=-=-00000000000')
    # очередь = [(type: str, content: typle), ...]
    #   type='func':    очередь = [('func', (func, args: list, kwargs: dict)), ...]
    #   type='ev':   очередь = [('ev', (type_ev:str, data:dict, func, args, kwargs)), ...] (ev - событие)
    #   type='text':   очередь = [('text', (text: str, data: dict)), ...]  data - словарь из пришедшего сообщения
    #   text='???':     очередь = [('content', (type:str, (data), peer_id:int, )), ...]
    #   type='cooking_msg'      = [('cooking_msg', msg: dict), ...]
    #   type='change_param'      = [('change_param', (peer_id, text, data: dict)), ...] data - словарь с обновленными параметрами
    #   type='inner_info'        = [('inner_info', (type, data)), ...]
    #       proc - для отправки в класс обработки сообщений
    #       db - для отправки в класс базы данных
    #       type_ev = [new_msg - новое сообщение]

    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info', 'fff']
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}]
    print('-0-0-0-0000)))')
    print(cpu_count())
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])
        for i in chains_mps}
    print('98********************')
    users_data1 = ['admins', 'developers']
    # {admins: {admin_id: session: bool, ...}, developers: {dev_id: bool, ...}, ...}
    users_data = Manager().dict()
    print('0&&&&&&&&&^&^^^')
    print('rffff')
    print('898*******---------')
    users_data['developers'] = {}
    #asasas = Manager().dict()
    print('898*******')
    users_data['admins'] = {}
    print('887&&^^%%$$##')


    # for i in users_data1:
    #     print('bhbhbj', i)
    #     users_data[str(i)] = Manager().dict()
    #     print('6^^^^^')
    # print('0-090898')
    # users_data = {i: Manager().dict() for i in users_data1}
    # dddd = Manager().dict()

    # =======! Создание общих частей для классов-родителей !=======
    print('&^%%%%%%%%%%%')
    BaseClass.common_start(queues=chains_mps, types=types)
    print('9^$$#####@@')
    VkBase.common_start()
    print('--------------------')
    # =======! Start working !=======
    r = [pool.apply_async(i.start, kwds={'vip_users': users_data, 'queues': chains_mps, 'types': types},
                          error_callback=error_callback_func) for i in [VkListen, VkSending]]
    r.extend([pool.apply_async(i.start, kwds={'queues': chains_mps, 'types': types},
                               error_callback=error_callback_func) for i in [ProcessingMsg, ControlDB]])
    [i.ready() for i in r]
    while True:
        sleep(1)
