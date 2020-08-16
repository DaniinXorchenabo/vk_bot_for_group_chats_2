from time import sleep
from re import (
    sub as re_sub,
    split as re_split
)
from random import randint
from functools import wraps

if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)
