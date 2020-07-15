from subprocess import Popen, CREATE_NEW_CONSOLE
from time import sleep

p_list = []
clients = 3


while True:
    user = input(f'launch the server and {clients} clients (s) / Close all (x) / Exit (q) ')

    if user == 'q':
        break
    elif user == 's':
        p_list.append(Popen(f'python server.py', creationflags=CREATE_NEW_CONSOLE))
        sleep(1)
        for i in range(clients):
            sleep(1 / clients)
            p_list.append(Popen(f'python client.py -a localhost -p 7777 -u user{i}', creationflags=CREATE_NEW_CONSOLE))
        print(f'launched {clients} clients')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
