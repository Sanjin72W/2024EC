int Velocity(int Target,int encoder_left,int encoder_right)
{
	static int Err_Lowout_Last,Encoder_S;//a为低通滤波系数，0.7为常见的系数
	static float a=0.1;
	int Err,Err_Lowout,temp;
	//1、计算偏差值
	Err=(encoder_left+encoder_right)-Target;
	//2、低通滤波
	Err_Lowout=(1-a)*Err+a+Err_Lowout_Last;
	Err_Lowout_Last=Err_Lowout;
}

通过一定比例接收下一次的误差从而实现低通滤波