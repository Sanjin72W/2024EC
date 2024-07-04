示例控制程序
void PID_Init(PID_TypeDef *pid)
{
    pid->target_val = 0.0;
    pid->actual_val = 0.0;
    pid->err = 0.0;
    pid->err_last = 0.0;
    pid->integral = 0.0;
    pid->Kp = 1.0;  // 设置比例系数
    pid->Ki = 0.0;  // 设置积分系数
    pid->Kd = 0.0;  // 设置微分系数
}

int main(void)
{
    // 初始化PID控制器参数
    PID_Init(&pid_angle);

    // 设置目标值，比如目标角度为30度
    pid_angle.target_val = 30.0;

    while (1)
    {
        // 获取当前的yaw值
        yaw = get_current_yaw();

        // 计算控制输出
        float control_output = Angle_pid_control(yaw);
    }
}
