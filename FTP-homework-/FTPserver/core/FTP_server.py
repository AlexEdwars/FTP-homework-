import socketserver
import os
import sys
import pickle


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


from FTPserver.function import upload
from FTPserver.function import download
from FTPserver.function import dir
from FTPserver.core import Config
from FTPserver.function import cd
from FTPserver.function import RegetUpload
from FTPserver.function import RegetDownload


class MySockerServer(socketserver.BaseRequestHandler):

    def handle(self):
        while 1:
            conn = self.request
            try:
                conn.sendall(bytes('连接成功', 'utf8'))
                print(str(conn.recv(1024), 'utf8'))
                conn.sendall(bytes('I\'m ok', 'utf8'))
                userid = str(conn.recv(1024), 'utf8')
                conn.sendall(bytes('all right', 'utf8'))
                username = str(conn.recv(1024), 'utf8')
                globals()['%s_cwd' %(username)] = os.path.join(Config.BASE_DIR, 'UserData\\%s' %(userid))
            except ConnectionResetError:
                break
            while 1:
                try:
                    cmd_recv = conn.recv(1024)
                except ConnectionResetError:
                    break
                try:
                    cmd, file = str(cmd_recv, 'utf8').split(' ')
                except Exception:
                    try:
                        cmd, course, file = str(cmd_recv, 'utf8').split(' ')
                    except Exception:
                        cmd = str(cmd_recv, 'utf8')
                if cmd == 'upload':
                    upload.run(file, conn)
                elif cmd == 'reget_upload':
                    RegetUpload.run(file, conn)
                elif cmd == 'download':
                    download.run(course, conn)
                elif cmd == 'reget_download':
                    RegetDownload.run(course, conn)
                elif cmd == 'dir':
                    username = str(conn.recv(1024), 'utf8')
                    dir.run(globals()['%s_cwd' %(username)], conn)
                elif cmd == 'info':
                    with open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\UserData' %(userid)), 'rb') as f:
                        userdata = pickle.loads(f.read())
                    for i in userdata:
                        conn.sendall(bytes('%s: %s' %(i, userdata[i]), 'utf8'))
                        conn.recv(1024)
                elif cmd == 'cd':
                    if file == 'user':
                        conn.sendall(bytes('Yeah', 'utf8'))
                        userid = str(conn.recv(1024), 'utf8')
                        conn.sendall(bytes('Yeah', 'utf8'))
                        username = str(conn.recv(1024), 'utf8')
                        globals()['%s_cwd' % (username)] = cd.run(globals()['%s_cwd' % (username)], file, conn, userid)
                    else:
                        username = str(conn.recv(1024), 'utf8')
                        globals()['%s_cwd' %(username)] = cd.run(globals()['%s_cwd' %(username)], file, conn)


sk = socketserver.ThreadingTCPServer(('127.0.0.1', 8000), MySockerServer)
sk.serve_forever()
