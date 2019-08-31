import mss
import mss.tools
import numpy as np
import cv2
import time
import imutils

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
    with mss.mss() as sct:
        monitor = {"top":150,"left":0,"width":670,"height":600}
        last_time = time.time()
        while(True):
            # 800x600 windowed mode
            printscreen =  cv2.cvtColor(np.array(sct.grab(monitor)),cv2.COLOR_BGR2RGB)
            if topLeft_clicked:
                cv2.circle(printscreen, center=pt1, radius=5, color=(0,0,255), thickness=-1)

            #drawing rectangle
            if topLeft_clicked and botRight_clicked:
                cv2.rectangle(printscreen, pt1, pt2, (0, 0, 255), 2)


#             print('loop took {} seconds'.format(time.time()-last_time))
#             last_time = time.time()
            cv2.imshow('frame',printscreen)
            if(flag == 1 or ((topLeft_clicked == True) and (botRight_clicked == True))):
                cv2.destroyAllWindows()
                break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
        last_time = time.time()
        monitor = {"top":pt1[1]+150,"left":pt1[0],"width":pt2[0]-pt1[0],"height":pt2[1]-pt1[1]}
        while(True):
            printroi =  np.array(sct.grab(monitor))
            gray_roi = cv2.cvtColor(printroi,cv2.COLOR_BGR2GRAY)
#             print('fps {}'.format(1/(time.time()-last_time)))
            ret,thresh = cv2.threshold(gray_roi,127,255,cv2.THRESH_BINARY_INV)
            x = 0 #The value of symmetry
            extr = findExtremes(thresh)
            extRight = tuple(extr[extr[:, :, 0].argmax()][0])
            extTop = tuple(extr[extr[:, :, 1].argmin()][0])
            extBot = tuple(extr[extr[:, :, 1].argmax()][0])
            shape_roi = gray_roi.shape
            cv2.line(printroi,(extRight[0],0),(extRight[0],extBot[1]),(255,0,0),1)
            cv2.line(printroi,(0,extTop[0]),(shape_roi[1],extTop[0]),(0,255,0),1)
            cv2.line(printroi,(0,extBot[0]),(shape_roi[1],extBot[0]),(0,0,255),1)
            
#             last_time = time.time()
            cv2.imshow('frame',cv2.cvtColor(printroi, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
                
def findExtremes(img):
    
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    return c
    
    
screen_record()