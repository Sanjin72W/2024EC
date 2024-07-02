#include "motor.h"

//motor1 2 һ�� 3 4 һ��

#define GPIO_GROUP_A		GPIOB
#define GPIO_GROUP_B
#define GPIO_GROUP_C		
#define GPIO_GROUP_D
#define GPIO_MOTOR_A_S1	GPIO_PIN_13
#define GPIO_MOTOR_A_S2	GPIO_PIN_12
#define GPIO_MOTOR_B_S1
#define GPIO_MOTOR_B_S2
#define GPIO_MOTOR_C_S1	
#define GPIO_MOTOR_C_S2	
#define GPIO_MOTOR_D_S1
#define GPIO_MOTOR_D_S2

#define PWM_MAX 16800
#define PWM_MIN -16800

extern TIM_HandleTypeDef htim4;
//extern uint8_t stop;//�����ź������ⲿ

int abs(int p)
{
	if(p>0)
		return p;
	else
		return -p;
}

void Load(int moto1,int moto2,int moto3,int moto4)			//-16800~16800
{
	if(moto1<0)
	{
		HAL_GPIO_WritePin(GPIO_GROUP_A,GPIO_MOTOR_A_S1,GPIO_PIN_SET);
		HAL_GPIO_WritePin(GPIO_GROUP_A,GPIO_MOTOR_A_S2,GPIO_PIN_RESET);
	}
	else
	{
		HAL_GPIO_WritePin(GPIO_GROUP_A,GPIO_MOTOR_A_S2,GPIO_PIN_RESET);
		HAL_GPIO_WritePin(GPIO_GROUP_A,GPIO_MOTOR_A_S1,GPIO_PIN_SET);
	}
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_1,abs(moto1));
	
//	if(moto2<0)
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_B,GPIO_MOTOR_B_S1,GPIO_PIN_SET);
//		HAL_GPIO_WritePin(GPIO_GROUP_B,GPIO_MOTOR_B_S2,GPIO_PIN_RESET);
//	}
//	else
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_B,GPIO_MOTOR_B_S2,GPIO_PIN_RESET);
//		HAL_GPIO_WritePin(GPIO_GROUP_B,GPIO_MOTOR_B_S1,GPIO_PIN_SET);
//	}
//	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_2,abs(moto2));
	
	//	if(moto3<0)
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_C,GPIO_MOTOR_C_S2,GPIO_PIN_SET);
//		HAL_GPIO_WritePin(GPIO_GROUP_C,GPIO_MOTOR_C_S1,GPIO_PIN_RESET);
//	}
//	else
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_C,GPIO_MOTOR_C_S1,GPIO_PIN_RESET);
//		HAL_GPIO_WritePin(GPIO_GROUP_C,GPIO_MOTOR_C_S2,GPIO_PIN_SET);
//	}
//	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_3,abs(moto3));

//	if(moto4<0)
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_D,GPIO_MOTOR_D_S2,GPIO_PIN_SET);
//		HAL_GPIO_WritePin(GPIO_GROUP_D,GPIO_MOTOR_D_S1,GPIO_PIN_RESET);
//	}
//	else
//	{
//		HAL_GPIO_WritePin(GPIO_GROUP_D,GPIO_MOTOR_D_S1,GPIO_PIN_RESET);
//		HAL_GPIO_WritePin(GPIO_GROUP_D,GPIO_MOTOR_D_S2,GPIO_PIN_SET);
//	}
//	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_4,abs(moto4));
}


void Stop()
{
		Load(0,0,0,0);
}
