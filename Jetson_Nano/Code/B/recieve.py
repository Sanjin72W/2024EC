import serial

# 串口设置
ser = serial.Serial('/dev/ttyTHS1', baudrate=115200, timeout=0)  

def print_without_newline(text):
    print(text, end='')

while True:
    try:
        # 尝试读取设备发送的数据
        data = ser.readline().decode('utf-8').strip()
        
        # 如果读取到数据，则打印到终端
        if data:
            print("Received:", data)
    
    except KeyboardInterrupt:
        # 按下Ctrl+C键停止程序
        print("Program stopped.")
        break

    except serial.SerialException:
        # 处理串口异常
        print("Error: Could not read from the serial port.")
        break

# 关闭串口连接
ser.close()
