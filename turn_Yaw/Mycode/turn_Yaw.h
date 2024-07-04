#ifndef _TURN_YAW_H
#define _TURN_YAW_H

#include "stm32f4xx_hal.h"

typedef struct {
    float target_val;
    float actual_val;
    float err;
    float err_last;
    float integral;
    float Kp, Ki, Kd;
} PID_TypeDef;

float Angle_pid_control(float yaw);

#endif
