import os


def run(cwd, sk_obj):
    data_list = os.listdir(cwd)
    file_num = len(data_list)
    sk_obj.sendall(bytes(str(file_num), 'utf8'))
    sk_obj.recv(1024)
    for i in data_list:
        sk_obj.sendall(bytes(i, 'utf8'))
        sk_obj.recv(1024)
