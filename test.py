import pickle
import hashlib

password = hashlib.sha512('f9285005zyf'.encode())

with open('static/lastlogin.txt', 'wb') as file:
    file.write(b'False\n')
    file.write(pickle.dumps({'login': 'HashFunction', 'password': password.hexdigest()}))

data = []

with open('static/lastlogin.txt', 'rb') as file:
    data.extend(file.readlines())

if data[0] == b'True\n':
    print(pickle.loads(data[-1]))
