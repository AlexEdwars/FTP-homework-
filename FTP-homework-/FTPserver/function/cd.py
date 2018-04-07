import os
from FTPserver.core import Config


def run(cwd, path, sk_obj, userid=None):
    if path == 'server':
        cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sk_obj.sendall(bytes('chdir successfully!', 'utf8'))
        return cwd
    elif path == 'user':
        cwd = os.path.join(Config.BASE_DIR, 'UserData\\%s' %(userid))
        sk_obj.sendall(bytes('chdir successfully!', 'utf8'))
        return cwd
    else:
        path = os.path.join(cwd, path)
    if not os.path.isdir(path):
        sk_obj.sendall(bytes('Error', 'utf8'))
        return cwd
    else:
        if path == os.path.join(Config.BASE_DIR, 'FTPserver\\..'):
            sk_obj.sendall(bytes('Error', 'utf8'))
            return cwd
        sk_obj.sendall(bytes('chdir successfully!', 'utf8'))
        return path
