import mediapipe as mp
import numpy as np
import pickle
import cv2
import pandas as pd
import csv  
from pythonosc import udp_client
import threading

OSC_IP = "192.168.8.185"  # Replace with your OSC server's IP address
OSC_PORT = 5002  # Replace with your OSC server's port

# Set desired resolution
width, height = 1280, 720

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

num_coords = 0
landmarks = []
mp_drawing = mp.solutions.drawing_utils

# Load the pre-trained model
with open('body_language.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to calculate angle
def calculate_angle(a, b, c):
    
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    if a is None or b is None or c is None:
        return "Unknown"
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

# Function to check if arms are above or below the torso
def check_arm_position(shoulder_landmark, elbow_landmark, wrist_landmark, hip_landmark):
    if shoulder_landmark is None or elbow_landmark is None or wrist_landmark is None or hip_landmark is None:
        return "Unknown"
    
    return "Above" if (elbow_landmark.y < hip_landmark.y and wrist_landmark.y < hip_landmark.y) else "Below"

# Function to check if hand is open or closed
def check_hand_openness(hand_landmarks, elbow_y):
    if hand_landmarks is None or elbow_y is None:
        return "Unknown"

    # Get the y-coordinate of the index finger tip
    index_tip_y = hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
    
    # Get the y-coordinate of the middle finger tip
    middle_tip_y = hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y
    
    # Determine if the hand is above or below the elbow
    hand_above_elbow = index_tip_y < elbow_y and middle_tip_y < elbow_y
    
    if hand_above_elbow:
        # If hand is above elbow
        if index_tip_y < middle_tip_y:
            return "Closed"
        else:
            return "Open"
    else:
        # If hand is below elbow
        if index_tip_y < middle_tip_y:
            return "Open"
        else:
            return "Closed"

    return "Unknown"


def send_data_through_osc(body_language_class, body_language_prob):
    client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)
    client.send_message("/aggressiveness", 1 if body_language_class == 'Aggressive' else 0)
    client.send_message("/prediction_accuracy", round(body_language_prob[np.argmax(body_language_prob)], 2))




# Configure holistic model for hand and body detection
with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if frame reading fails

        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Make Detections
        results = holistic.process(image)

        if num_coords == 0:
            num_coords = 42  # Default value if no landmarks are detected initially

            if results.pose_landmarks:
                num_coords += len(results.pose_landmarks.landmark)
            if results.face_landmarks:
                num_coords += len(results.face_landmarks.landmark)

            for val in range(1, num_coords + 1):
                landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val), ]

            with open('coords.csv', mode='a', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(landmarks)

        class_name = "Aggressive"

        # Draw right hand landmarks
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                    )
            right_hand_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                        results.right_hand_landmarks.landmark]).flatten())
        else:
            right_hand_row = [0] * 21 * 4

        # Draw left hand landmarks
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                    )
            left_hand_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                        results.left_hand_landmarks.landmark]).flatten())
        else:
            left_hand_row = [0] * 21 * 4


        try:
            if results.pose_landmarks and results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP] and results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]:
                landmarks = results.pose_landmarks.landmark
                    
                left_shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y]
                    
                right_shoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]
                    
                left_hip = [landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                    
                left_arm_position = check_arm_position(landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value],
                                                       landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value],
                                                       landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value],
                                                       landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value])

                right_arm_position = check_arm_position(landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value],
                                                        landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value],
                                                        landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value],
                                                        landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value])

                left_hand_openness = check_hand_openness(results.left_hand_landmarks, landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y)
                right_hand_openness = check_hand_openness(results.right_hand_landmarks, landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y)
                    

                # Get the y-coordinate of the head landmark
                head_y = landmarks[mp_holistic.PoseLandmark.NOSE.value].y if landmarks[mp_holistic.PoseLandmark.NOSE.value] else None

                # Calculate the aggression probability based on the conditions
                aggression_probability = 0
                
                if left_arm_angle < 95:
                    aggression_probability += 0.3

                if right_arm_angle < 95:
                    aggression_probability += 0.3
                
                if left_arm_position == "Above":
                    if head_y and left_wrist[1] < head_y:  # Check if wrist is higher than head
                        aggression_probability += 0.05
                if right_arm_position == "Above":
                    if head_y and right_wrist[1] < head_y:  # Check if wrist is higher than head
                        aggression_probability += 0.05
                
                if left_hand_openness == "Closed":
                    aggression_probability += 0.15

                if right_hand_openness == "Closed":
                    aggression_probability += 0.15


            if results.pose_landmarks:
                pose_landmarks = results.pose_landmarks.landmark
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                           )

                pose_row = list(
                    np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                              pose_landmarks]).flatten())

            row = pose_row + left_hand_row + right_hand_row

            X = pd.DataFrame([row])
            body_language_class = model.predict(X)[0]
            body_language_prob = model.predict_proba(X)[0]
            #print(body_language_class, body_language_prob)

            coords = tuple(np.multiply(np.array((pose_landmarks[mp.solutions.holistic.PoseLandmark.LEFT_EAR].x,
                                                  pose_landmarks[mp.solutions.holistic.PoseLandmark.LEFT_EAR].y,)),
                                       [640, 480]).astype(int))
            cv2.rectangle(image, (coords[0], coords[1] + 5), (coords[0] + len(body_language_class) * 20, coords[1] - 30),
                          (245, 117, 16), -1)

            cv2.putText(image, body_language_class, coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

            cv2.putText(image, 'CLASS', (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, body_language_class[0], (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                        cv2.LINE_AA)

            cv2.putText(image, 'ACURAT', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2)), (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            send_data_through_osc(body_language_class, body_language_prob)

        except Exception as e:
            print("Error:", e)

        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
