from multiprocessing import Pool, Queue, cpu_count, Lock, Manager


if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split


    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
