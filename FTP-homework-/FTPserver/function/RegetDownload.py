import os
from FTPserver.core import Config


def run(course, sk_obj):
    userid = str(sk_obj.recv(1024), 'utf8')
    sk_obj.sendall(bytes('userid get', 'utf8'))
    course = os.path.join(Config.BASE_DIR, 'UserData\\%s\\%s' %(userid, course))
    sk_obj.sendall(bytes(str(os.stat(course).st_size), 'utf8'))
    try:
        data_recv = int(str(sk_obj.recv(1024), 'utf8'))
    except Exception:
        return None
    with open(course, 'rb') as f:
        f.seek(data_recv + 1)
        data = f.read()
    sk_obj.sendall(data)
    sk_obj.recv(1024)
