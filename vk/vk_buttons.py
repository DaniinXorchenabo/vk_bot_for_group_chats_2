import json


def create_all_button(*strings, name=None):
    print(")(((((()()()( --- ", strings)
    strings = [[((i, 'primary') if type(i) == str else i)
                for i in ([string] if type(string) == str else string)]
               for string in strings]
    print(*strings, sep="\n")
    button = {
        "one_time": True,
        "buttons": [
            [create_button(*button) for button in string]
            for string in strings
        ]}
    button = json.dumps(button, ensure_ascii=False).encode('utf-8')
    if not name:
        return str(button.decode('utf-8'))


# доп функция для кнопок (так удобнее)
def create_button(label, color, payload=''):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


class VkButton():
    colors = {'pr': 'primary', 's': 'secondary', 'n': 'negative', 'p': 'positive'}

    def __init__(self, lable='', color='pr', _type='text', payload=''):
        """

        :param lable: текст кнопки
        :param color: цвет кнопки [pr, s, n, p]
        :param type: ["text", 'open_link', 'Location', 'callback']
        :param payload: при нажатии кнопки вернется строка с указанным содержимым
        """
        self.color = VkButton.colors[color]
        self.lable = lable
        self.type = _type
        self.payload = payload

    def get_dict(self):
        _dict = {"action": {
            "type": self.type,
            "payload": self.payload,
            "label": self.lable
        }, "color": self.color}
        return _dict


class RowForKeyBoard():

    def __init__(self, *texts, color='pr', _type='text', payload=''):
        self.row = [VkButton(text, color, _type, payload) for text in texts]

    def __iter__(self):
        self.row_iter = iter(self.row)
        return self.row_iter

    def __next__(self):
        return next(self.row_iter)


class KeyBoard():
    def __init__(self, *rows, one_time=True, inline=False):
        self.rows = rows
        self.one_time = one_time
        self.inline = inline

    def add_row(self, row):
        self.rows.append(row)
        list.extend()

    def add_rows(self, *rows):
        self.rows.extend(rows)

    def get_dict(self):
        struct = {"one_time": self.one_time,
                "buttons": [[button.get_dict() for button in row] for row in self.rows],
                "inline": self.inline
                }
        if self.inline:
            del struct['one_time']
        return json.dumps(struct, ensure_ascii=False).encode('utf-8')


row1 = RowForKeyBoard('помощь', 'расшифровка')
row2 = RowForKeyBoard('/gen', '/er', '/st')
row3 = RowForKeyBoard('/n_kw', '/kw')
standart_kw_cl = KeyBoard(row1, row2, row3, one_time=False)
del_keyboard = KeyBoard()
