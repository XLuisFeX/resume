#Import modules
import cv2
import mediapipe as mp
import time

#Mediapipe solutions to use
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

#Def hand detector class
class HandDetector:
    
    #Init hands solution with settings
    def __init__(self, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5):
        self.hands = mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

    #Def findLandMarks functions. This funcion detect hand in input image
    def findHandLandMarks(self, image, handNumber=0, draw=False):
        
        left_fingers=[0,0,0,0,0] #left hand array, each value represent a finger, it could be 0 or 1
        right_fingers=[0,0,0,0,0] #Right hand array, each value represent a finger, it could be 0 or 1
        left_landMarkList=[] #Left hand landmarks positions
        right_landMarkList=[] #Right hand landmarks positions

        originalImage = image #Copy input image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Conver image to RGB
        results = self.hands.process(image) #Find hands in image
        
        if results.multi_hand_landmarks:  # returns None if hand is not found
            for handNumber in range(0,len(results.multi_handedness)): #for each hand detected
                    landMarkList = []
                    label = results.multi_handedness[handNumber].classification[0].label #Detect if is left or right hand
                    if label == "Left":
                        label = "Right"
                    elif label == "Right":
                        label = "Left"
                    hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands
                    for id, landMark in enumerate(hand.landmark):
                        # landMark holds x,y,z ratios of single landmark
                        imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                        xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                        if(label=='Left'):
                            left_landMarkList.append([id, xPos, yPos, label]) #append landmark id, x position, y position and label
                        if(label=='Right'):
                            right_landMarkList.append([id, xPos, yPos, label]) #append landmark id, x position, y position and label
                        
                       
                    if(label=='Left'): #Count up fingers for left hand
                        if left_landMarkList[4][3] == "Right" and left_landMarkList[4][1] > left_landMarkList[3][1]:       #Right Thumb
                            left_fingers[0]=1
                        elif left_landMarkList[4][3] == "Left" and left_landMarkList[4][1] < left_landMarkList[3][1]:       #Left Thumb
                            left_fingers[0]=1
                        if left_landMarkList[8][2] < left_landMarkList[6][2]:       #Index finger
                            left_fingers[1]=1
                        if left_landMarkList[12][2] < left_landMarkList[10][2]:     #Middle finger
                            left_fingers[2]=1
                        if left_landMarkList[16][2] < left_landMarkList[14][2]:     #Ring finger
                            left_fingers[3]=1
                        if left_landMarkList[20][2] < left_landMarkList[18][2]:     #Little finger
                            left_fingers[4]=1  
                            
                    if(label=='Right'): #Count up fingers for right hand
                        if right_landMarkList[4][3] == "Right" and right_landMarkList[4][1] > right_landMarkList[3][1]:       #Right Thumb
                            right_fingers[0]=1
                        elif right_landMarkList[4][3] == "Left" and right_landMarkList[4][1] < right_landMarkList[3][1]:       #Left Thumb
                            right_fingers[0]=1
                        if right_landMarkList[8][2] < right_landMarkList[6][2]:       #Index finger
                            right_fingers[1]=1
                        if right_landMarkList[12][2] < right_landMarkList[10][2]:     #Middle finger
                            right_fingers[2]=1
                        if right_landMarkList[16][2] < right_landMarkList[14][2]:     #Ring finger
                            right_fingers[3]=1
                        if right_landMarkList[20][2] < right_landMarkList[18][2]:     #Little finger
                            right_fingers[4]=1  
                        
        if results.multi_hand_landmarks: #Draw hand landmarks on image
            for hand_landmarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(originalImage, hand_landmarks, mpHands.HAND_CONNECTIONS, 
                                                mpDraw.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                                mpDraw.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                                                 )

        return left_fingers, right_fingers, left_landMarkList, right_landMarkList

#Set videocapture from webcam
cap = cv2.VideoCapture(0)

#if not cap.isOpened():
#    raise IOError('Cannot open cam')

font_scale = 2 #Set fontScale
font = cv2.FONT_HERSHEY_PLAIN #Set font

#Initialize hand detecto class
handDetector = HandDetector(min_detection_confidence=0.7)

#Run code until 'q' key is pressed or close hand gesture detected
while True:
    
    #read webcam frame
    ret, frame = cap.read()
    
    #Apply hand landmarks detection to frame
    L_fingers, R_fingers, L_handLandmarks, R_handLandmarks = handDetector.findHandLandMarks(image=frame, draw=True)

    
    #Hand gestures detection
    if(L_fingers==[0, 1, 0, 0, 1]):
        cv2.putText(frame, 'Left hand: Rock on!', (100, 100),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        
    if(L_fingers==[0, 1, 1, 0, 0]):
        cv2.putText(frame, 'Left hand: Peace&Love', (100, 100),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        
    if(R_fingers==[0, 1, 0, 0, 1]):
        cv2.putText(frame, 'Right hand: Rock on!', (100, 400),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        
    if(R_fingers==[0, 1, 1, 0, 0]):
        cv2.putText(frame, 'Right hand: Peace&Love', (100, 400),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        
    if(L_fingers==[1, 0, 1, 0, 0]):
        x1=L_handLandmarks[9][1]
        y1=L_handLandmarks[9][2]
        
        x2=L_handLandmarks[12][1]
        y2=L_handLandmarks[12][2]
        
        R = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
        
        cv2.circle(frame, (x1,y1), radius=R, color=(255, 255, 255), thickness=-1)
        cv2.putText(frame, 'Left hand: F#@k you', (100, 100),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        
    if(R_fingers==[1, 0, 1, 0, 0]):
        x1=R_handLandmarks[9][1]
        y1=R_handLandmarks[9][2]
        
        x2=R_handLandmarks[12][1]
        y2=R_handLandmarks[12][2]
        
        R = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
        
        cv2.circle(frame, (x1,y1), radius=R, color=(255, 255, 255), thickness=-1)
        cv2.putText(frame, 'Right hand: F#@k you', (100, 100),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)   
    
    
    if(R_fingers==[0, 1, 0, 0, 0] and L_fingers==[1, 1, 1, 1, 1]):
        cv2.putText(frame, 'EXIT', (100, 400),font, fontScale=font_scale, color=(255, 255, 255), thickness=2)
        cv2.destroyAllWindows()
        break

        
    #Draw output frame
    cv2.imshow('Output', frame)

    #Stop execution 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

        
cap.release()
cv2.destroyAllWindows()