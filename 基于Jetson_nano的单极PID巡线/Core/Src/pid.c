#include "pid.h"
#include "encoder.h"
#include "motor.h"

#define Target_xunji_max 200
#define Target_xunji_min -200
int PWM_Stand=800;

//闭环控制中间变量
int Xunji_out,Target_Speed,Target_xunji,MOTO1,MOTO2;

//参数
float Xunji_Kp=-100,Xunji_Kd=-0.65,Xunji_Ki;			//直立环 数量级（Kp：0~1000、Kd：0~10）

int pidabs(int p)
{
	if(p>0)
		return p;
	else
		return -p;
}

//循迹环PID控制器
//输入：期望速度、左编码器、右编码器
int Xunji(int Err_data)
{
	static int Err_LowOut_last,Encoder_S;
	static float a=0.7;
	int Err,Err_LowOut,temp;
	Xunji_Ki=Xunji_Kp/200;
	//1、计算偏差值
	Err=Err_data;
	//2、低通滤波
	Err_LowOut=(1-a)*Err+a*Err_LowOut_last;
	//3、积分
	Encoder_S+=Err_LowOut;
	//4、积分限幅(-300~300)
	Encoder_S=Encoder_S>300?300:(Encoder_S<(-300)?(-300):Encoder_S);
	//5、循迹环计算
	temp=Xunji_Kp*Err_LowOut+Xunji_Ki*Encoder_S+Xunji_Kd*(Err_LowOut-Err_LowOut_last);
	Err_LowOut_last=Err_LowOut;
	return temp;
}

void Limit_Target(int *motoA)
{
	if(*motoA>Target_xunji_max)*motoA=Target_xunji_max;
	if(*motoA<Target_xunji_min)*motoA=Target_xunji_min;
}


void Control(void)	//每隔10ms调用一次
{	
	if(rec_data.aim_or_not=='Y')
	{
			Target_xunji=Xunji(pidabs(rec_data.xunji));
			Limit_Target(&Target_xunji);
			//在屏幕左边，左拐，右边加速
			if(rec_data.xunji>0)
				{
					MOTO1=PWM_Stand-Target_xunji;
					MOTO2=PWM_Stand+Target_xunji;
					Limit(&MOTO1,&MOTO2);
					Load(MOTO1,MOTO2);
				}
			//在屏幕右边，右拐，左边加速
			if(rec_data.xunji<=0)
				{
				MOTO1=PWM_Stand+Target_xunji;
				MOTO2=PWM_Stand-Target_xunji;
				Limit(&MOTO1,&MOTO2);
				Load(MOTO1,MOTO2);
				}
	}
	if(rec_data.aim_or_not=='N'){
		Load(0,0);
	}
}
