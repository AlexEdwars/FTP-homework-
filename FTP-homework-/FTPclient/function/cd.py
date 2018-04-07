from FTPclient.core import user_status


user_status = user_status.user_status


def run(username, sk_obj):
    sk_obj.sendall(bytes(username, 'utf8'))
    data = str(sk_obj.recv(1024), 'utf8')
    if data == 'Error':
        print('无此目录')
    else:
        print()
