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
        if str(sk_obj.recv(1024),'utf8') == 'Error':
            print('文件超出剩余空间!')
            return None
        with open(file, 'rb') as file:
            data = file.read()
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