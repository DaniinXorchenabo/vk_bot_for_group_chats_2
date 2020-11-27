# -*- coding: utf-8 -*-

from time import sleep
from re import (
    sub as re_sub,
    split as re_split
)
from random import randint
from functools import wraps
from os import getcwd, chdir, environ
from os.path import isfile, join, split as os_split

if __name__ == '__main__':
    from os.path import split as os_split

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    chdir(path)
