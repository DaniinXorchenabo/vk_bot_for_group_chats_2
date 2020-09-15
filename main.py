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
    from multiprocessing import Pool, cpu_count, Manager

    # =======! initialization !=======
    pool = Pool(processes=5)
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
    types = ['func', "ev", "text", 'content', 'cooking_msg', 'change_param', 'inner_info']
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}]
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])
        for i in chains_mps}
    users_data = ['admins', 'developers']
    # {admins: {admin_id: session: bool, ...}, developers: {dev_id: bool, ...}, ...}
    users_data = {i: Manager().dict() for i in users_data}

    # =======! Создание общих частей для классов-родителей !=======
    BaseClass.common_start(queues=chains_mps, types=types)
    VkBase.common_start()

    # =======! Start working !=======
    r = [pool.apply_async(i.start, kwds={'vip_users': users_data, 'queues': chains_mps, 'types': types},
                          error_callback=error_callback_func) for i in [VkListen, VkSending]]
    r.extend([pool.apply_async(i.start, kwds={'queues': chains_mps, 'types': types},
                               error_callback=error_callback_func) for i in [ProcessingMsg, ControlDB]])
    [i.ready() for i in r]
    while True:
        sleep(1)
