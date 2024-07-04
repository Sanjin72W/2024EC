#include "turn_Yaw.h"

float low_Fliter(float yaw);

/**
 * @brief  �ǶȻ�PID�������
 * @param  pid: PID�ṹ��ָ��
 * @param  actual_val: ʵ��ֵ 6050yaw
 * @retval ͨ��PID���������
 */
float Angle_pid_realize(PID_TypeDef *pid, float actual_val)
{
    /* ����ƫ�� */
    pid->err = pid->target_val - actual_val;

    if (pid->err > 180) // ��ֹС��ת��180��ʱһֱ��ת������
        pid->err = pid->err - 360;
    if (pid->err < -180)
        pid->err = pid->err + 360;

    pid->integral += pid->err; // ����ۻ�

    /* PID�㷨ʵ�� */
    pid->actual_val = pid->Kp * pid->err + pid->Ki * pid->integral + pid->Kd * (pid->err - pid->err_last);

    /* ���� */
    pid->err_last = pid->err;

    /* ���ص�ǰʵ��ֵ */
    return pid->actual_val;
}

/* ȫ�ֱ��� */
PID_TypeDef pid_angle;
float yaw;

/**
 * @brief  �ǶȻ�PID���ƺ���
 * @retval ͨ��PID���������
 */
float Angle_pid_control(float yaw)
{
    float Expect_Pwm = 0.0; // ��ǰ����ֵ

    /* ����� KLM ���������Ƕ� yaw �����˲� */
    float Pid_Actual_angle;
	Pid_Actual_angle = low_Fliter(yaw); // ʵ��ֵ Ϊ yaw �˲��������

    /* ���� PID ���� */
    Expect_Pwm = Angle_pid_realize(&pid_angle, Pid_Actual_angle);

    return Expect_Pwm;
}

float low_Fliter(float yaw)
{
    static float yaw_Lowout_Last = 0.0f; // ��ʼ����һ���˲������ֵ
    static float a = 0.1f; // ��ͨ�˲�ϵ��
    float yaw_Lowout, temp;
    
    temp = yaw;
    yaw_Lowout = a * yaw_Lowout_Last + (1 - a) * temp;
    yaw_Lowout_Last = yaw_Lowout;

    return yaw_Lowout;
}
