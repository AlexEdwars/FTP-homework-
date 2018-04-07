from FTPclient.core import user_status


user_status = user_status.user_status


def run(sk_obj):
    sk_obj.sendall(bytes(user_status['username'], 'utf8'))
    file_num = int(str(sk_obj.recv(1024), 'utf8'))
    sk_obj.sendall(bytes('file_size get!', 'utf8'))
    file_recv = 0
    data = []
    while file_num > file_recv:
        data.append(str(sk_obj.recv(1024), 'utf8'))
        file_recv += 1
        sk_obj.sendall(bytes('file get', 'utf8'))
    for i in data:
        print(i)
