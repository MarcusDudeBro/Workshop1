import pyautogui
import cv2
import mediapipe as mp
import keyboard

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# save screen size
s = pyautogui.size()

# Initialize webcam
cap = cv2.VideoCapture(1) 
while True:
    # capture webcame frame and shape (width and height)
    ret, frame = cap.read()
    x, y, c = frame.shape
    # defining the frame
    frame = cv2.flip(frame, 1)
    # have mediapipe hands predict hand landmarks
    result = hands.process(frame)
    # iterate through the predicted landmarks adjusting them to the window, and 
    # and outputting them to the opencv window
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            # take the 8th landmark (index finger point) and move the cursor to that landmarks x and y value
            pyautogui.moveTo(int(handslms.landmark[8].x * s[0]), int(handslms.landmark[8].y * s[1]), _pause=False)
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
    cv2.imshow('Output', frame)
    # if q is pressed, program exits
    if cv2.waitKey(1) == ord('q'):
        break
    if keyboard.is_pressed('q'):
        break
cap.release()
cv2.destroyAllWindows()