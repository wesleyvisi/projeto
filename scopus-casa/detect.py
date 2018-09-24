import sys
import numpy as np
import cv2
import time


video_capture = cv2.VideoCapture("rtsp://10.42.0.93:554/user=admin&password=admin&channel=1&stream=1.sdp?")

time.sleep(1.0)

ret, frame = video_capture.read()
bg = frame;



while 1:
    ret, frame = video_capture.read()
    
    new = cv2.absdiff(bg, frame)
    
    new = cv2.dilate(new, None, iterations=10)
    
    
    cv2.imshow("Video",new)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('n'):
            
        ret, frame = video_capture.read()
        bg = frame;
    
    
video_capture.release()
cv2.destroyAllWindows()