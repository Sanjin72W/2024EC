import socket

# Jetson Nano的IP地址和端口号
SERVER_IP = '172.20.10.14'
SERVER_PORT = 888

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
server_socket.bind((SERVER_IP, SERVER_PORT))

# 开始监听连接
server_socket.listen(1)
print("等待MSP430连接...")

# 接受MSP430连接
client_socket, client_address = server_socket.accept()
print("MSP430已连接：", client_address)

while True:
    greet ="hello 430!"
    client_socket.sendall(greet.encode())
    # 接收MSP430发送的数据
    data = client_socket.recv(1024)
    if not data:
        break
    print("接收到来自MSP430的数据：", data.decode())

    # 处理数据（根据需要进行相应的处理逻辑）

    # 发送响应数据给MSP430
    response = "收到来自MSP430的数据：" + data.decode()
    client_socket.sendall(response.encode())

# 关闭连接
client_socket.close()
server_socket.close()


