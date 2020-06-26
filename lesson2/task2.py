"""
Задача 2.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
"""

import json


ORDER_FILE = 'data/orders.json'


def write_to_json(item, quantity, price, buyer, date):
    dict_repr = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
    }

    with open(ORDER_FILE, 'r') as o_f:
        order_list = json.load(o_f)

    if 'orders' in order_list.keys():
        order_list['orders'].append(dict_repr)

    with open(ORDER_FILE, 'w', newline='') as o_f:
        json.dump(order_list, o_f, indent=4)


write_to_json('One piece dress', 1, 1000, 'Anne Rose', '18-06-2020')
with open(ORDER_FILE, 'r') as o_f:
    print(o_f.read())
