import sys
import numpy as np
import cv2
import time


video_capture = cv2.VideoCapture("rtsp://10.42.0.93:554/user=admin&password=admin&channel=1&stream=1.sdp?")

print("carregando... 0")
time.sleep(0.3)
print("carregando... 20")
time.sleep(0.3)
print("carregando... 40")
time.sleep(0.3)
print("carregando... 60")
time.sleep(0.3)
print("carregando... 80")
time.sleep(0.3)
print("carregando... 100")

ret, frame = video_capture.read()
bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);






while 1:
    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    new = cv2.absdiff(bg, gray)
    
    new = cv2.dilate(new, None, iterations=2)
    
    new = cv2.threshold(new, 55, 255, cv2.THRESH_BINARY)[1]
    
    new = cv2.dilate(new, np.ones((6,3), np.uint8), iterations=5)
    
    _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 45*45:
            #crop_img = frame[y:y+h, x:x+w]
            
            for cy in range(y,y+h):
                for cx in range(x,x+w):
                    bg[cy,cx] = gray[cy,cx]
            
            continue
        
        
        if cv2.contourArea(contour) < 60*60:
            continue
        
        
        color = (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    
    
 
    cv2.imshow("NEW",new)
    cv2.imshow("Frame",frame)
    cv2.imshow("bg",bg)
    
    if cv2.waitKey(1) & 0xFF == ord('n'):     
        cv2.destroyAllWindows()
        ret, frame = video_capture.read()
        bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video_capture.release()
cv2.destroyAllWindows()