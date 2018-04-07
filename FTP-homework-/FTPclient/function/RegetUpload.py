import os
import sys
from FTPclient.core import Config
from FTPclient.core import user_status


user_status = user_status.user_status


def run(file, sk_obj):
    if not os.path.isabs(file):
        file = os.path.join(Config.BASE_DIR, 'FTP_client\\core\\%s' % (file))
    if not os.path.isfile(file):
        print('命令错误')
    else:
        userid = user_status['userid']
        file_size = os.stat(file).st_size
        sk_obj.sendall(bytes(str(file_size), 'utf8'))
        sk_obj.recv(1024)
        sk_obj.sendall(bytes(userid, 'utf8'))
        try:
            data_recv = int(str(sk_obj.recv(1024), 'utf8'))
        except Exception:
            print('请使用upload')
            return None
        with open(file, 'rb') as f:
            f.seek(data_recv + 1)
            data = f.read()
        sk_obj.sendall(bytes(str(len(data)), 'utf8'))
        sk_obj.recv(1024)
        sk_obj.sendall(data)
        progess = 0
        progess_times = int(str(sk_obj.recv(1024), 'utf8'))
        for i in range(progess_times):
            progess_inside = str(sk_obj.recv(1024), 'utf8')
            try:
                for i in range(int(progess_inside)):
                    sys.stdout.write('*')
                sys.stdout.flush()
                progess += int(progess_inside)
            except Exception:
                break
        print()
        print('上传成功')

