#Import modules
import cv2
import numpy as np

#Def make invisible function, this function recive webcam frame, background image and color ranges to remove
def make_invisible(frame,background):
    
    #Change frame from BGR to HSV colorspace
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #Get parameters from Trackbars
    l_h = cv2.getTrackbarPos("L_H","Parameters")
    l_s = cv2.getTrackbarPos("L_S","Parameters")
    l_v = cv2.getTrackbarPos("L_V","Parameters")
    u_h = cv2.getTrackbarPos("U_H","Parameters")
    u_s = cv2.getTrackbarPos("U_S","Parameters")
    u_v = cv2.getTrackbarPos("U_V","Parameters")
    
    #Create numpay array for lower and upper colors in HSV colorspace
    l_hsv = np.array([l_h, l_s, l_v])
    u_hsv = np.array([u_h, u_s, u_v])

    #Detect area where color range is present in webcam frame
    mask = cv2.inRange(hsv_frame, l_hsv, u_hsv)

    #Using mask to select background portions to keep
    part1 = cv2.bitwise_and(background, background, mask=mask)

    #Detect area where color range is NOT present in webcam frame
    color_free = cv2.bitwise_not(mask)

    #Using color_free mask to select webcam frame portions to keep
    part2 = cv2.bitwise_and(frame, frame, mask=color_free)
    
    #Join the portions we want to keep
    output_frame = part1+part2
    
    return output_frame

#Set videocapture from webcam
cap = cv2.VideoCapture(0)

#Get background frame
for i in range(30):
    ret,back = cap.read()

#Def empty function for trackbars
def empty(a):
    pass

#Def trackbars window to set parameters
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",700,250)
cv2.createTrackbar("L_H","Parameters",65,179,empty)
cv2.createTrackbar("L_S","Parameters",128,255,empty)
cv2.createTrackbar("L_V","Parameters",143,255,empty)
cv2.createTrackbar("U_H","Parameters",255,179,empty)
cv2.createTrackbar("U_S","Parameters",255,255,empty)
cv2.createTrackbar("U_V","Parameters",255,255,empty)


#Run code until 'q' key is pressed
while cap.isOpened():
    
    #read webcam frame
    ret,frame = cap.read()
    
    #Apply make_invisible function
    output_img = make_invisible(frame,back)
    
    #Display result
    cv2.imshow("Final",output_img)
    
    #Stop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows() 
        cap.release()
        break