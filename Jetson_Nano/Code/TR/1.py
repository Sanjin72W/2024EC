import serial
import time

# 配置串口
ser = serial.Serial('/dev/ttyTHS1', 115200)

# 发送和接收数据
# data_to_send = b"+200\n"

# ser.write(data_to_send)  # 发送数据

# time.sleep(5)
# data_to_send = b"-200\n"

# ser.write(data_to_send)  # 发送数据

# time.sleep(5)
data_to_send = b"A\n"

ser.write(data_to_send)  # 发送数据

time.sleep(10)
# 关闭串口
ser.close()

# 打印发送和接收的数据
print("Sent: ", data_to_send)