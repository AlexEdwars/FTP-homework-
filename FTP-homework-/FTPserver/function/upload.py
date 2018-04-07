import os
import pickle
from FTPserver.core import Config


def run(file, sk_obj):
    try:
        file_name = file.split('\\')[-1]
    except Exception as e:
        file_name = file
    file_size = int(str(sk_obj.recv(1024), 'utf8'))
    sk_obj.sendall(bytes('file_size recv ok!', 'utf8'))
    userid = str(sk_obj.recv(1024), 'utf8')
    with open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\UserData' %(userid)), 'rb') as f:
        userdata = pickle.loads(f.read())
    if file_size > int(userdata['free_space']):
        sk_obj.sendall(bytes('Error', 'utf8'))
        return None
    sk_obj.sendall(bytes('userid recv ok!', 'utf8'))
    userdata['free_space'] -= file_size
    with open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\UserData' % (userid)), 'wb') as f:
        pickle.dump(userdata)
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
    if os.path.isfile(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, file_name))):
        with open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, file_name)), 'wb') as file:
            file.truncate()
    f = open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, file_name)), 'ab')
    for i in data:
        f.write(i)
    f.close()
