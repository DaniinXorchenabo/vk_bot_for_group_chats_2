if __name__ == '__main__':
    from multiprocessing import Pool, cpu_count, Manager

    pool = Pool(processes=5)
    # очередь = [(type: str, content: typle), ...]
    #   type='func':    очередь = [('func', (func, args: list, kwargs: dict)), ...]
    #   type='ev':   очередь = [('ev', (type_ev:str, data:dict, func, args, kwargs)), ...] (ev - событие)
    #   type='text':   очередь = [('text', (text: str, data: dict)), ...]  data - словарь из пришедшего сообщения
    #   text='???':     очередь = [('content', (type:str, (data): str, peer_id:int, )), ...]
    #       proc - для отправки в класс обработки сообщений
    #       db - для отправки в класс базы данных
    #       type_ev = [new_msg - новое сообщение]
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}]
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])
        for i in chains_mps}
    users_data = ['admins', 'developers']
    users_data = {i: Manager().dict() for i in users_data}  # {name: {id: session: bool, ...}, ...}


