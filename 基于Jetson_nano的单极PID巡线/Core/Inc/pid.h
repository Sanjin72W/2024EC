#ifndef __PID_H__
#define __PID_H__

#include "stm32f1xx_hal.h"

typedef struct {
    uint8_t option;
		int xunji;
		char aim_or_not;
} RecData;

extern RecData rec_data;

void Control(void);	//ÿ��10ms����һ��

#endif
