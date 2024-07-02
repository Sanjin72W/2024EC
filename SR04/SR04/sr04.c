#include "sr04.h"

#define	GPIO_GROUP 	GPIOE
#define	GPIO_ECHO 	GPIO_PIN_15
#define GPIO_TR		GPIO_PIN_14

uint16_t count;
float distance;
extern TIM_HandleTypeDef htim3;

void RCCdelay_us(uint32_t udelay)
{
  __IO uint32_t Delay = udelay * 168 / 8;
  do
  {
    __NOP();
  }
  while (Delay --);
}


void GET_Distance(void)
{
	HAL_GPIO_WritePin(GPIO_GROUP,GPIO_ECHO,GPIO_PIN_SET);
	RCCdelay_us(11);
	HAL_GPIO_WritePin(GPIO_GROUP,GPIO_ECHO,GPIO_PIN_RESET);
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	if(GPIO_Pin==GPIO_TR)
	{
		if(HAL_GPIO_ReadPin(GPIO_GROUP,GPIO_TR)==GPIO_PIN_SET)
		{
			__HAL_TIM_SetCounter(&htim3,0);
			HAL_TIM_Base_Start(&htim3);
		}
		else
		{
			HAL_TIM_Base_Stop(&htim3);
			count=__HAL_TIM_GET_COUNTER(&htim3);
			distance=count*0.017;
		}
	}
}
