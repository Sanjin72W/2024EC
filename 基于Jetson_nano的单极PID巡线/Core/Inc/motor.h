#ifndef _MOTOR_H
#define _MOTOR_H

#include "stm32f1xx_hal.h"
void Load(int moto1,int moto2);
void Limit(int *motoA,int *motoB);
void Stop(float *Med_Jiaodu,float *Jiaodu);

void Left_Moto(int mode);//×ó
void Right_Moto(int mode);//ÓÒ

void car_go_straight(void);
void car_go_right(void);
void car_go_left(void);
void car_stop(void);
void car_go_after(void);

#endif
