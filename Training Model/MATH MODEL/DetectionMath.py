import cv2
import mediapipe as mp
import numpy as np
from pythonosc import udp_client
import threading

OSC_IP = "172.16.20.82"  # Replace with your OSC server's IP address
OSC_PORT = 5001  # Replace with your OSC server's port

# Set desired resolution
width, height = 1280, 720

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

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


def send_data_through_osc(left_arm_angle, right_arm_angle, left_arm_position,
                          left_hand_openness, right_hand_openness, aggression_probability):
    client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)
    client.send_message("/left_arm_angle", left_arm_angle)
    client.send_message("/right_arm_angle", right_arm_angle)
    client.send_message("/left_arm_position", left_arm_position)
    client.send_message("/left_hand_openness", left_hand_openness)
    client.send_message("/right_hand_openness", right_hand_openness)
    client.send_message("/aggression_probability", aggression_probability)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
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
                    
                # Calculate the aggression probability based on the conditions
                aggression_probability = 0
                
                if left_arm_angle < 95:
                    aggression_probability += 0.3

                if right_arm_angle < 95:
                    aggression_probability += 0.3
                
                if left_arm_position == "Above":
                    aggression_probability += 0.1
                if right_arm_position == "Above":
                    aggression_probability += 0.1
                
                if left_hand_openness == "Closed":
                    aggression_probability += 0.1

                if right_hand_openness == "Closed":
                    aggression_probability += 0.1

                cv2.putText(image, f"Left Arm Angle: {left_arm_angle}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Arm Angle: {right_arm_angle}", (10, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Left Arm Position: {left_arm_position}", (10, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Arm Position: {right_arm_position}", (10, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Left Hand: {left_hand_openness}", (10, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Hand: {right_hand_openness}", (10, 300), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.putText(image, f"Aggression Probability: {aggression_probability * 100}%", (10, 350), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                    
                osc_thread = threading.Thread(target=send_data_through_osc, args=(
                    left_arm_angle, right_arm_angle, left_arm_position, 
                    left_hand_openness, right_hand_openness, aggression_probability
                ))
                osc_thread.start()
                
            else:
                # If shoulders are not detected, set aggressiveness to 0
                left_arm_angle = "Unknown"
                right_arm_angle = "Unknown"
                left_arm_position = "Unknown"
                right_arm_position = "Unknown"
                left_hand_openness = "Unknown"
                right_hand_openness = "Unknown"
                aggression_probability = 0
                
                cv2.putText(image, f"Left Arm Angle: {left_arm_angle}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Arm Angle: {right_arm_angle}", (10, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Left Arm Position: {left_arm_position}", (10, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Arm Position: {right_arm_position}", (10, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Left Hand: {left_hand_openness}", (10, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Right Hand: {right_hand_openness}", (10, 300), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Aggression Probability: {aggression_probability * 100}%", (10, 350), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                osc_thread = threading.Thread(target=send_data_through_osc, args=(
                    left_arm_angle, right_arm_angle, left_arm_position, 
                    left_hand_openness, right_hand_openness, aggression_probability
                ))
                osc_thread.start()
                
        except Exception as e:
            print(f"An error occurred: {e}")

        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
