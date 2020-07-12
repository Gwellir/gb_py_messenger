from subprocess import Popen, CREATE_NEW_CONSOLE
from time import sleep

p_list = []
count = 3

while True:
    user = input(f'launch {count} clients (s) / Close clients (x) / Exit (q) ')

    if user == 'q':
        break
    elif user == 's':
        for i in range(count):
            sleep(1/count)
            p_list.append(Popen(f'python client.py sender {i + 1} ', creationflags=CREATE_NEW_CONSOLE))
        print(f'launched {count} clients')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
