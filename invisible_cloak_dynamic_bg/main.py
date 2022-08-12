#Import modules
import cv2
import numpy as np
import time
import mediapipe as mp

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

#Initialize mediapipe selfie segmentation module
mp_selfie_segmentation = mp.solutions.selfie_segmentation

#Set videocapture from mp4 background video
cap_bg = cv2.VideoCapture('backgrounds/bg_video.mp4')
#Set videocapture from webcam
cap_live = cv2.VideoCapture(0)

#Get FPS to control speed
fps = int(cap_bg.get(cv2.CAP_PROP_FPS))

#Def empty function for trackbars
def empty(a):
    pass

#Def trackbars window to set parameters
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",700,250)
cv2.createTrackbar("L_H","Parameters",65,255,empty)
cv2.createTrackbar("L_S","Parameters",128,255,empty)
cv2.createTrackbar("L_V","Parameters",143,255,empty)
cv2.createTrackbar("U_H","Parameters",255,255,empty)
cv2.createTrackbar("U_S","Parameters",255,255,empty)
cv2.createTrackbar("U_V","Parameters",255,255,empty)

#Set selfie segmentation alias for loop
with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1) as selfie_segmentation: 
    
    #Run code until 'q' key is pressed
    while cap_bg.isOpened():

        #read mp4 background frame
        success_bg, image_bg = cap_bg.read()
        
        #Control speed
        time.sleep(1/fps)
        
        #Resize background frame
        image_bg = cv2.resize(image_bg, (640,480), interpolation = cv2.INTER_AREA)

        #read frame from webcam
        success_live, image_live = cap_live.read()

        #Convert webcam frame to RGB
        image_live = cv2.cvtColor(image_live, cv2.COLOR_BGR2RGB)

        #Apply selfie segmentation
        image_live.flags.writeable = False
        results = selfie_segmentation.process(image_live)
        image_live.flags.writeable = True
        
        #Convert frame to BGR
        image_live = cv2.cvtColor(image_live, cv2.COLOR_RGB2BGR)
        
        #Get selfie segmentation mask
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        
        #Apply mask to background frame
        output_image = np.where(condition, image_live, image_bg)
        
        #Apply make_invisible function
        output_image = make_invisible(output_image,image_bg)


        #Display result
        cv2.imshow('Output', output_image)

        #Stop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows() 
            cap_live.release()
            cap_bg.release()
            break
