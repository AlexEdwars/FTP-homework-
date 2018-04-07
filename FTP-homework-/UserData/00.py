import pickle


userdata = {
    'userid': '0002',
    'username': 'User02',
    'passwd': '123456',
    'space': 52428800,     # bytes
    'free_space': 52428800,     # bytes
    'status': 'normal'
}


f = open('0002\\UserData', 'wb')
pickle.dump(userdata, f)
f.close()
