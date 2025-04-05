from bluetooth import *

# 创建RFCOMM通道
server_socket = BluetoothSocket(RFCOMM)

# 监听端口
server_socket.bind(("", PORT_ANY))
server_socket.listen(1)

# 获取本地设备的蓝牙地址
server_address = server_socket.getsockname()[0]
print("本地设备地址:", server_address)

# 设置服务名称和UUID
service_name = "MyBluetoothService"
service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

# 将服务名称和UUID注册到SDP记录中
advertise_service(server_socket, service_name, service_uuid)

print("等待客户端连接...")

# 接受客户端连接
client_socket, client_address = server_socket.accept()
print("已连接到客户端:", client_address)

# 接收数据
data = client_socket.recv(1024)
print("接收到的数据:", data.decode())

# 发送数据
message = 'a'
client_socket.send(message.encode())
print("已发送数据:", message)

# 关闭连接
client_socket.close()
server_socket.close()
print("连接已关闭")
