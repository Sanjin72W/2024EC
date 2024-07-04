#include "turn_Yaw.h"

float low_Fliter(float yaw);

/**
 * @brief  角度环PID输出函数
 * @param  pid: PID结构体指针
 * @param  actual_val: 实际值 6050yaw
 * @retval 通过PID计算后的输出
 */
float Angle_pid_realize(PID_TypeDef *pid, float actual_val)
{
    /* 计算偏差 */
    pid->err = pid->target_val - actual_val;

    if (pid->err > 180) // 防止小车转到180度时一直旋转的问题
        pid->err = pid->err - 360;
    if (pid->err < -180)
        pid->err = pid->err + 360;

    pid->integral += pid->err; // 误差累积

    /* PID算法实现 */
    pid->actual_val = pid->Kp * pid->err + pid->Ki * pid->integral + pid->Kd * (pid->err - pid->err_last);

    /* 误差传递 */
    pid->err_last = pid->err;

    /* 返回当前实际值 */
    return pid->actual_val;
}

/* 全局变量 */
PID_TypeDef pid_angle;
float yaw;

/**
 * @brief  角度环PID控制函数
 * @retval 通过PID计算后的输出
 */
float Angle_pid_control(float yaw)
{
    float Expect_Pwm = 0.0; // 当前控制值

    /* 这里的 KLM 函数假设是对 yaw 进行滤波 */
    float Pid_Actual_angle;
	Pid_Actual_angle = low_Fliter(yaw); // 实际值 为 yaw 滤波后的数据

    /* 进行 PID 计算 */
    Expect_Pwm = Angle_pid_realize(&pid_angle, Pid_Actual_angle);

    return Expect_Pwm;
}

float low_Fliter(float yaw)
{
    static float yaw_Lowout_Last = 0.0f; // 初始化上一次滤波输出的值
    static float a = 0.1f; // 低通滤波系数
    float yaw_Lowout, temp;
    
    temp = yaw;
    yaw_Lowout = a * yaw_Lowout_Last + (1 - a) * temp;
    yaw_Lowout_Last = yaw_Lowout;

    return yaw_Lowout;
}
