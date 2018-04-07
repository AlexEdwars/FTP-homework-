import os
import sys
from FTPclient.core import user_status
from FTPclient.core import Config


user_status = user_status.user_status


def run(file, sk_obj):
    sk_obj.sendall(bytes(user_status['userid'], 'utf8'))
    sk_obj.recv(1024)
    if not os.path.isabs(file):
        file = os.path.join(Config.BASE_DIR, '\\FTPclient\\core\\%s' %(file))
    if os.path.isfile(file):
        with open(file, 'wb') as f:
            f.truncate()
    file_size = int(str(sk_obj.recv(1024), 'utf8'))
    sk_obj.sendall(bytes('file size get', 'utf8'))
    data = []
    file_recv = 0
    progess = 0
    while file_size > file_recv:
        data.append(sk_obj.recv(1024))
        file_recv += 1024
        progess_inside = file_recv // file_size
        progess_inside *= 100
        progess_inside -= progess
        for i in range(progess_inside):
            sys.stdout.write('*')
        sys.stdout.flush()
    f = open(file, 'ab')
    for i in data:
        f.write(i)
    f.close()
    print()
    sk_obj.sendall(bytes('下载成功', 'utf8'))
    print('下载成功')
