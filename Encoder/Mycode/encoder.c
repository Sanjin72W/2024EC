#include "encoder.h"

//-300`290

int Read_Speed(TIM_HandleTypeDef *htim)
{
	int temp;
	temp=(short)__HAL_TIM_GetCounter(htim);
	__HAL_TIM_SetCounter(htim,0);
	return temp;
}
