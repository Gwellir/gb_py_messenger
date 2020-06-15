# Задача 2.
# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

byte_words = [b'class', b'function', b'method']

for bword in byte_words:
    print(type(bword), bword, bword.decode(encoding='utf-8'), len(bword))
