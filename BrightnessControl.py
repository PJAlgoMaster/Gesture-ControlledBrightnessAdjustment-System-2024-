import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import face_recognition
import pickle
import os
import subprocess
from math import hypot
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

if not os.path.exists('authorized_encoding.pkl'):
    print("Error: Please run Script 2 to create the authorized encoding file.")
    speak("Error: Please run Script 2 to create the authorized encoding file.")
    exit()

with open('authorized_encoding.pkl', 'rb') as f:
    authorized_encoding = pickle.load(f)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)
Draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source")
    exit()

authenticated = False
assistant_process = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not authenticated:
        face_locations = face_recognition.face_locations(frameRGB)
        face_encodings = face_recognition.face_encodings(frameRGB, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([authorized_encoding], face_encoding)
            if True in matches:
                authenticated = True
                print("User authenticated")
                speak("User authenticated")
                if assistant_process is None or assistant_process.poll() is not None:
                    assistant_process = subprocess.Popen(["python", "personal_assistant.py"])
                break
        if not authenticated:
            cv2.putText(frame, "Unauthorized User", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
    else:
        if assistant_process is None or assistant_process.poll() is not None:
            assistant_process = subprocess.Popen(["python", "personal_assistant.py"])

    Process = hands.process(frameRGB)

    landmarkList = []
    if Process.multi_hand_landmarks:
        for handlm in Process.multi_hand_landmarks:
            for _id, landmarks in enumerate(handlm.landmark):
                height, width, color_channels = frame.shape
                x, y = int(landmarks.x * width), int(landmarks.y * height)
                landmarkList.append([_id, x, y])

            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

    if len(landmarkList) >= 9:
        x_1, y_1 = landmarkList[4][1], landmarkList[4][2]
        x_2, y_2 = landmarkList[8][1], landmarkList[8][2]

        cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)
        cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

        L = hypot(x_2 - x_1, y_2 - y_1)
        b_level = np.interp(L, [15, 220], [0, 100])

        sbc.set_brightness(int(b_level))

    cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if assistant_process is not None:
    assistant_process.terminate()
