import cv2
import mediapipe as mp
import serial
import math
import tensorflow as tf
import warnings

# Remove error messages
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')
tf.get_logger().setLevel('ERROR')

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize serial connection with Arduino
arduino = serial.Serial(port='/dev/tty.usbmodem101', baudrate=9600, timeout=.1)

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    ba = [a.x - b.x, a.y - b.y]
    bc = [c.x - b.x, c.y - b.y]
    cosine_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (
                math.sqrt(ba[0] ** 2 + ba[1] ** 2) * math.sqrt(bc[0] ** 2 + bc[1] ** 2))
    angle = math.acos(cosine_angle)
    return math.degrees(angle)


# Function to map angle to servo angle
def map_value(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)


# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame and get hand landmarks
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Define landmarks for each finger's joints
            finger_joints = {
                'thumb': [hand_landmarks.landmark[2], hand_landmarks.landmark[3], hand_landmarks.landmark[4]],
                'index': [hand_landmarks.landmark[5], hand_landmarks.landmark[6], hand_landmarks.landmark[8]],
                'middle': [hand_landmarks.landmark[9], hand_landmarks.landmark[10], hand_landmarks.landmark[12]],
                'ring': [hand_landmarks.landmark[13], hand_landmarks.landmark[14], hand_landmarks.landmark[16]],
                'pinky': [hand_landmarks.landmark[17], hand_landmarks.landmark[18], hand_landmarks.landmark[20]],
            }

            servo_angles = []

            # Calculate angles for each finger and determine if fully bent
            for finger, joints in finger_joints.items():
                angle = calculate_angle(joints[0], joints[1], joints[2])
                if angle > 160:  # Adjust threshold for fully bent finger
                    servo_angle = 180  # Fully bent
                else:
                    servo_angle = 0  # Not bent
                servo_angles.append(servo_angle)

            # Send angles to Arduino
            angles_str = ",".join(map(str, servo_angles)) + "\n"
            arduino.write(bytes(angles_str, 'utf-8'))

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
