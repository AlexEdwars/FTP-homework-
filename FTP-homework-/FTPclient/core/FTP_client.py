import os
import sys
import socket


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


from FTPclient.login import login
from FTPclient.core import user_status
from FTPclient.function import upload
from FTPclient.function import download
from FTPclient.function import dir
from FTPclient.function import cd
from FTPclient.function import RegetUpload
from FTPclient.function import RegetDownload


login.login()

sk = socket.socket()
address = ('127.0.0.1', 8000)
sk.connect(address)
print(str(sk.recv(1024), 'utf8'))
sk.sendall(bytes('%s已连接' %(user_status.user_status['username']), 'utf8'))
sk.recv(1024)
sk.sendall(bytes(user_status.user_status['userid'], 'utf8'))
sk.recv(1024)
sk.sendall(bytes(user_status.user_status['username'], 'utf8'))

while 1:
    user_inp = input('>>>:(输入-help查看帮助)').strip()
    if not user_inp:
        print('请不要输入空值')
        continue
    elif user_inp == '-help':
        print('帮助列表'.center(20, '-'))
        print('''
        upload file:上传文件
        download file:下载文件
        dir: 显示目录内文件/目录
        cd dir:进入目录
        info:显示个人信息
        reget_upload file: 断点续传
        reget_download file: 断点续下载
        exit():退出
        ''')
        print('帮助列表'.center(20, '-'))
    elif user_inp == 'exit()':
        exit()
    else:
        if user_inp == 'dir':
            sk.sendall(bytes(user_inp, 'utf8'))
            dir.run(sk)
        elif user_inp == 'info':
            sk.sendall(bytes(user_inp, 'utf8'))
            for i in range(6):
                print(str(sk.recv(1024), 'utf8'))
                sk.sendall(bytes('next', 'utf8'))
        else:
            try:
                cmd, file = user_inp.split(' ')
            except Exception:
                try:
                    cmd, course, file = user_inp.split(' ')
                except Exception:
                    print('命令错误')
                    continue
            if cmd == 'upload':
                sk.sendall(bytes(user_inp, 'utf8'))
                upload.run(file, sk)
            elif cmd == 'reget_upload':
                sk.sendall(bytes(user_inp, 'utf8'))
                RegetUpload.run(file, sk)
            elif cmd == 'download':
                sk.sendall(bytes(user_inp, 'utf8'))
                download.run(file, sk)
            elif cmd == 'reget_download':
                sk.sendall(bytes(user_inp, 'utf8'))
                RegetDownload.run(file, sk)
            elif cmd == 'cd':
                sk.sendall(bytes(user_inp, 'utf8'))
                if file == 'user':
                    sk.recv(1024)
                    sk.sendall(bytes(user_status.user_status['userid'], 'utf8'))
                    sk.recv(1024)
                cd.run(user_status.user_status['username'], sk)
            else:
                print('命令错误')
