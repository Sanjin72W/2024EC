import cv2
cap=cv2.VideoCapture('/dev/video0')
fc=cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml')
if not cap.isOpened():
	print("false to open")
	exit()

while True:
	ret,frame=cap.read()
	
	print(frame.shape)

	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	faces=fc.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)

	for(x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	
	cv2.imshow('USB',frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
cap.release()
cv2.destroyALLWindows()

