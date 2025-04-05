import socket

SERVER_IP = '172.20.10.14'
SERVER_PORT = 8888

# 创建TCP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client_socket.connect((SERVER_IP, SERVER_PORT))
print('Connected to server:', SERVER_IP, SERVER_PORT)

# 发送和接收数据
while True:
    message = input('Enter a message: ')
    client_socket.send(message.encode())  # 发送数据给服务器
    
    response = client_socket.recv(1024)  # 接收服务器响应
    print('Server response:', response.decode())
    
    if message.lower() == 'bye':
        # 结束通信
        print('Closing connection')
        break

# 关闭套接字连接
client_socket.close()
