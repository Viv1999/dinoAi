import numpy as np
import cv2
import time
import pyscreenshot as ImageGrab

pt1 = (0,0)
pt2 = (0,0)
topLeft_clicked = False
botRight_clicked = False
flag = 0

def draw_rectangle(event,x,y,flags,param):

    global pt1,pt2,topLeft_clicked,botRight_clicked,flag

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if topLeft_clicked == True and botRight_clicked == True:
            topLeft_clicked = False
            botRight_clicked = False
            flag = 1
            pt1 = (0,0)
            pt2 = (0,0)

        if topLeft_clicked == False:
            pt1 = (x,y)
            topLeft_clicked = True
            
        elif botRight_clicked == False:
            pt2 = (x,y)
            botRight_clicked = True

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rectangle)

    

def screen_record():
    last_time = time.time()
    while(True):
        # 800x600 windowed mode
        printscreen =  cv2.cvtColor(np.array(ImageGrab.grab(bbox = (0,80,600,800))),cv2.COLOR_BGR2RGB)
        if topLeft_clicked:
            cv2.circle(printscreen, center=pt1, radius=5, color=(0,0,255), thickness=-1)
        
        #drawing rectangle
        if topLeft_clicked and botRight_clicked:
            cv2.rectangle(printscreen, pt1, pt2, (0, 0, 255), 2)
        
        
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('frame',printscreen)
        if(flag == 1 or ((topLeft_clicked == True) and (botRight_clicked == True))):
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    last_time = time.time()
    while(True):
        printroi =  np.array(ImageGrab.grab(bbox = (pt1[0],pt1[1]+80,pt2[0],pt2[1]+80)))
        print('loop took {} seconds'.format(time.time()-last_time))
        ret,thresh = cv2.threshold(printroi,127,255,cv2.THRESH_BINARY_INV)
        last_time = time.time()
        cv2.imshow('frame',cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()