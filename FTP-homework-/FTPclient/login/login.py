import os
import pickle
from FTPclient.core import user_status
from FTPclient.core import Config


def login():
    if not user_status.user_status['statu']:
        times = 0
        while times < 3:
            userid = input('UserID:').strip()
            passwd = input('Passwd:').strip()
            if not os.path.isfile(os.path.join(Config.BASE_DIR, 'UserData\\%s\\UserData' %(userid))):
                print('用户名或密码错误!')
                times += 1
            else:
                with open(os.path.join(Config.BASE_DIR, 'UserData\\%s\\UserData' %(userid)), 'rb') as file:
                    userdata = pickle.loads(file.read())
                if not passwd == userdata['passwd']:
                    print('用户名或密码错误!')
                    times += 1
                else:
                    user_status.user_status['statu'] = True
                    user_status.user_status['userid'] = userdata['userid']
                    user_status.user_status['username'] = userdata['username']
                    print('登录成功!')
                    break
        else:
            print('错误次数太多,账户已被锁定')
            exit()
    else:
        print('已登录')
