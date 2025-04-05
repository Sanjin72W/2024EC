import cv2
cap=cv2.VideoCapture('/dev/video0')
if not cap.isOpened():
	print("false to open")
	exit()

while True:
	ret,frame=cap.read()
	
	cv2.imshow('USB',frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
cap.release()
cv2.destroyALLWindows()

