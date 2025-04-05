import simple_pid
import time

# 初始化PID参数
Kp = 1.0  # 比例控制参数
Ki = 0.1  # 积分控制参数
Kd = 0.01  # 微分控制参数

# 设定目标转速
target_speed = 800  # 目标转速为100 rpm

# 初始化PID控制器
pid_controller = simple_pid.PID(Kp, Ki, Kd, setpoint=target_speed)

# 模拟电机转速
current_speed = 0

# 模拟电机控制循环
for i in range(100):
    # 获取当前转速（这里用随机数模拟）
    current_speed += (target_speed - current_speed) * 0.2  # 模拟电机响应时间
    print("Current Speed:", current_speed)

    # 计算PID控制量
    control = pid_controller(current_speed)
    print("Control:",control)
    # 在实际应用中，将控制量应用到电机上，控制其转速
    # motor.set_speed(control)

    # 模拟控制周期
    time.sleep(0.001)

print("PID control finished.")
