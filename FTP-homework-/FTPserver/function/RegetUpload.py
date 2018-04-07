import os
from FTPserver.core import Config


def run(file, sk_obj):
    try:
        file_name = file.split('\\')[-1]
    except Exception as e:
        file_name = file
    file_size = int(str(sk_obj.recv(1024), 'utf8'))
    sk_obj.sendall(bytes('file_size recv ok!', 'utf8'))
    userid = str(sk_obj.recv(1024), 'utf8')
    if os.path.isfile(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, file_name))):
        data_recv = os.stat(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, file_name))).st_size
        if data_recv >= file_size:
            sk_obj.sendall(bytes('请使用upload', 'utf8'))
            return None
    else:
        sk_obj.sendall(bytes('请使用upload', 'utf8'))
        return None
    sk_obj.sendall(bytes(str(data_recv), 'utf8'))
    file_size = int(str(sk_obj.recv(1024), 'utf8'))
    sk_obj.sendall(bytes('get', 'utf8'))
    file_recv = 0
    data = []
    progess = 0
    progess_times = (file_size // 1024)
    sk_obj.sendall(bytes(str(progess_times), 'utf8'))
    while file_size > file_recv:
        data.append(sk_obj.recv(1024))
        file_recv += 1024
        progess_inside = file_recv // file_size
        progess_inside *= 100
        progess_inside -= progess
        sk_obj.sendall(bytes(str(progess_inside), 'utf8'))
    sk_obj.sendall(bytes('OK', 'utf8'))
    f = open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' % (userid, file_name)), 'ab')
    for i in data:
        f.write(i)
    f.close()
