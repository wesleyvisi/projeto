
import numpy as np
import cv2
import time
import sys



def verificaArea(q1,q2):
    x1 = q1[0]
    y1 = q1[1]
    w1 = q1[2]
    h1 = q1[3]
    
    x2 = q2[0]
    y2 = q2[1]
    w2 = q2[2]
    h2 = q2[3]
    
    x = -1
    y = -1
    w = -1
    h = -1
    
    
    
    if((x1 > x2) & ((x2 + w2) > x1) ):
        if((y1 > y2) & ((y2 + h2) > y1) ):
            
            
            w = x2 + w2 - x1
            if(w1 < w):
                w = w1
            x = x1
            
            h = y2 + h2 - y1
            if(h1  < h):
                h = h1
                
            y = y1
                
            

            
            
        elif((y1 <= y2) & (y2 <= (y1 + h1 )) ):
            
            
            w = x2 + w2 - x1
            if(w1 < w):
                w = w1
                
            x = x1
            
            h = y1 + h1 - y2
            if(h2  < h):
                h = h2
                
            y = y2

            
          
            
    elif((x1 <= x2) & (x2 <= (x1 + w1 )) ):
        if((y1 > y2) & ((y2 + h2) > y1) ):
            
            
            w = x1 + w1 - x2
            if(w2 < w):
                w = w2
                
            x = x2
            
            h = y2 + h2 - y1
            if(h1  < h):
                h = h1
                
            y = y1
                
            

            
          
        elif((y1 <= y2) & (y2 <= (y1 + h1 )) ):
            
            
            w = x1 + w1 - x2
            if(w2 < w):
                w = w2
                
            x = x2
            
            h = y1 + h1 - y2
            if(h2  < h):
                h = h2
                
            y = y2
                
    
    
    if(w == -1 & h == -1):
        return False
    
    A1 = w1 * h1
    A2 = w2 * h2
    A = w * h
    
    
    
    
    if((A > (A1 * 0.2)) | (A > (A2 * 0.2))):
        return True
    
    else:
        return False

            
          
         









video_capture = cv2.VideoCapture("rtsp://10.42.0.93:554/user=admin&password=admin&channel=1&stream=1.sdp?")

print("carregando... 0")
time.sleep(0.3)

cascPath = "haarcascade_upperbody.xml"
upperbodyCascade = cv2.CascadeClassifier(cascPath)

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

cont = 0

lista = []




while 1:
    cont = cont +1
    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    new = cv2.absdiff(bg, gray)
    
    new = cv2.dilate(new, None, iterations=2)
    
    new = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)[1]
    
    new = cv2.dilate(new, np.ones((9,3), np.uint8), iterations=5)
    
    _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if ((cv2.contourArea(contour) < 50*50) & (w < (h * 4)) & (w > (h * 0.20)) ):
            #crop_img = frame[y:y+h, x:x+w]
            
            for cy in range(y,y+h):
                for cx in range(x,x+w):
                    bg[cy,cx] = gray[cy,cx]
            
            continue
        
        
        if cv2.contourArea(contour) < 60*60:
            continue
        
        
        
        color = (0, 255, 0)
        
        salva = True
        for nitem in range(0, len(lista)):
            
            item = lista[nitem]
            
            #if ((x > (item[0] - 70)) & (x < (item[0] + 70))) & ((y > (item[1] - 70)) & (y < (item[1] + 70)) & ((x + w)  > (item[0] - 70 + item[2])) & ((x + w) < (item[0] + 70 + item[2]))) & (((y+h) > (item[1] - 70 + item[3])) & ((y+h) < (item[1] + 70 + item[3]))):
            
            if(verificaArea(item,[x, y, w, h])):
            
            #if ((x + w > item[0])):
            
                novoitem = [x, y, w, h, item[4],[item[0],item[1],item[2],item[3]],item[6]]
                
                lista.pop(nitem)
                
                lista.insert(nitem,novoitem)
                salva = False
                
                continue
            
            
            if(verificaArea(item[5],[x, y, w, h])):
            
                    
                if x > item[0]:
                    x = item[0]
                    
                if y > item[1]:
                    y = item[1]
                    
                if x + w < item[0] + item[2]:
                    w = (item[0] + item[2]) - x
                    
                if y + h < item[1] + item[3]:
                    h = (item[1] + item[3]) - y
                    
                
            
                novoitem = [x, y, w, h, item[4],item[5],item[6]]
                
                lista.pop(nitem)
                
                lista.insert(nitem,novoitem)
                salva = False
                
                
                continue
            
            
        
            
        
        
        if(salva):
            lista.append([x, y, w, h,cont,[x, y, w, h],False])
            
            
    
    
    
    
    for nitem in range(0, len(lista)):
        
        
        
        item = lista[nitem]
        
        x = item[0]
        y = item[1]
        w = item[2]
        h = item[3]
        
        
        if(item[6] == False & (cont % 5 == 0)):
            quadro = gray[y:y+h, x:x+w]

            upperbodys = upperbodyCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=3)
            
            for (ux, uy, uw, uh) in upperbodys:
                item[6] = True
                    
                lista.pop(nitem)
                    
                lista.insert(nitem,item)
            
            
        
        cv2.putText(frame, "{}".format(item[4]), (x, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        if item[6]:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50,150,50), 2)
        
    
    
    
    
    
    
    print(len(lista))
 
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
