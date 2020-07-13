from subprocess import Popen, CREATE_NEW_CONSOLE
from time import sleep

p_list = []
senders = 5
listeners = 2


while True:
    user = input(f'launch {senders} + {listeners} clients (s) / Close clients (x) / Exit (q) ')

    if user == 'q':
        break
    elif user == 's':
        for i in range(senders):
            sleep(1 / senders)
            p_list.append(Popen(f'python client.py sender {i + 1} ', creationflags=CREATE_NEW_CONSOLE))
        print(f'launched {senders} emitters')
        for i in range(listeners):
            p_list.append(Popen(f'python client.py listen', creationflags=CREATE_NEW_CONSOLE))
        print(f'launched {senders} listeners')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
