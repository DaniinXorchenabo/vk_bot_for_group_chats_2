if __name__ == '__main__':
    from os import getcwd
    from os.path import split as os_split
    from processing.processing_messenges import ProcessingMsg

    path = os_split(getcwd())
    path = os_split(path[0])[0] if not bool(path[-1]) else path[0]
    print(path)


@ProcessingMsg.command('/new_msg', pr=-1)
def new_msg_proc(cls, type_ev, text, peer_id, *args, queues=dict(), **kwargs):
    if type(text) == list:
        text = ' '.join(text)
    _dict = dict()
    start_w_dict = dict()
    for part in (part.split() for part in
                 iter(re_sub(r'()([.!?\n]{1,})',
                             r'\1 \2 #@*`~', re_sub(r'([^.,!:;? ])()([.,!:?;\n]{1,})', r'\1 \2 \3',
                                                    re_sub(r'''[«»{}\][()"'*#$^~`]''', '', text.lower()))).split(
                     '#@*`~'))
                 if len(part.split()) > 0):
        if len(part) == 1:
            part += ['.']
        for i in range(1, len(part) - 1):
            _dict[part[i]] = _dict.get(part[i], cls.Counter()) + cls.Counter({part[i + 1]: 1})
        start_w_dict[part[0]] = start_w_dict.get(part[0], cls.Counter()) + cls.Counter({part[1]: 1})
        _dict[part[-1]] = start_w_dict.get(part[-1], cls.Counter())
    content = [start_w_dict, _dict]
    # chat_id =
    cls.put_db('content', '/new_msg', (start_w_dict, _dict), peer_id, queues=queues, pr=-1)
