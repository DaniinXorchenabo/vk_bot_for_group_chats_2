if __name__ == '__main__':
    from base.base_libs import *

    pool = Pool(processes=5)
    # очередь = [(type: str, content: typle), ...]
    #   type='func':    очередь = [('func', (func, args: list, kwargs: dict)), ...]
    #   type='event':   очередь = [('event', (type_ev:str, data:dict, func, args, kwargs)), ...]
    chains_mps = ['send', 'listen', 'start', {'proc': 2}, {'db': 2}]
    chains_mps = {(i if type(i) != dict else list(i.keys())[0]): (
        Manager().Queue() if type(i) != dict else [Manager().Queue() for _ in range(list(i.values())[0])])
        for i in chains_mps}


