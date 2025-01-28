# authentication.py
import cv2
import face_recognition
import pickle
import os

def capture_and_encode_face(username):
    cap = cv2.VideoCapture(0)
    print(f"Capturing face for {username}... Please make sure your face is visible on the camera.")
    ret, frame = cap.read()

    if ret:
        print("Face captured successfully")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(frame_rgb)

        if face_encodings:
            user_encoding = face_encodings[0]
            if os.path.exists('user_encodings.pkl'):
                with open('user_encodings.pkl', 'rb') as f:
                    user_encodings = pickle.load(f)
            else:
                user_encodings = {}

            user_encodings[username] = user_encoding

            with open('user_encodings.pkl', 'wb') as f:
                pickle.dump(user_encodings, f)
            print(f"{username}'s face encoding has been saved successfully!")
        else:
            print("No face detected in the captured image. Please try again.")
    else:
        print("Failed to capture image from the camera.")
    
    cap.release()
    cv2.destroyAllWindows()
