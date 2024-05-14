import csv
import numpy as np
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

num_coords = 0

landmarks = ['class']

# Replace 'your_video_file.mp4' with the path to your video file
video_file = r"C:\Users\carme\OneDrive\Escritorio\term3\MICROCHALLENGE\Videos\Agressive_final.mp4"
cap = cv2.VideoCapture(video_file)

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if frame reading fails

        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Make Detections
        results = holistic.process(image)

        if num_coords == 0:
            num_coords = len(results.pose_landmarks.landmark) + 42 if results.pose_landmarks else 42  # 21 landmarks for each hand, if not detected, 0 values will be added

            for val in range(1, num_coords + 1):
                landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val), ]

            with open('coords.csv', mode='a', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(landmarks)

        class_name = "Aggressive"

        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw Pose Landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            )

        # 2. Right hand
        if results.right_hand_landmarks:
            right_hand_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                          results.right_hand_landmarks.landmark]).flatten())
        else:
            print("Right hand not detected")
            right_hand_row = [0] * 21 * 4  # 21 landmarks with 4 coordinates each

        # 3. Left Hand
        if results.left_hand_landmarks:
            left_hand_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                          results.left_hand_landmarks.landmark]).flatten())
        else:
            print("Left hand not detected")
            left_hand_row = [0] * 21 * 4  # 21 landmarks with 4 coordinates each

        # 4. Pose Detections
        if results.pose_landmarks:
            pose_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in
                          results.pose_landmarks.landmark]).flatten())
        else:
            print("Pose landmarks not detected")
            pose_row = [0] * 33 * 4  # 33 landmarks with 4 coordinates each

        # Export coordinates
        try:
            # Adding landmarks all together
            row = pose_row + left_hand_row + right_hand_row
            row.insert(0, class_name)

            with open('coords.csv', mode='a', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(row)

        except Exception as e:
            print("Error:", e)

        out.write(image)
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
