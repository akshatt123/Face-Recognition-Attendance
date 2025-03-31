import cv2
import numpy as np
import face_recognition
from datetime import datetime
from face_recognition_utils import load_known_faces, mark_attendance
from app import app 


# Load known faces
known_faces, known_names = load_known_faces()
print(f"Loaded {len(known_faces)} known faces.")

# Global variables for camera
cap = None      
running = False

def start_camera():
    """Start Face Recognition and stream frames."""
    global cap, running


    if running:
        print("Camera is already running.")
        return
    
    cap = cv2.VideoCapture(0)
    running = True

    while running:
        success, frame = cap.read()
        if not success:
            # print("Failed to capture frame")
            continue

        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, encoding)
            name = "Unknown"

            if any(matches):
                face_distances = face_recognition.face_distance(known_faces, encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index].upper()

            # Scale back location since we resized earlier
            top, right, bottom, left = [val * 4 for val in location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Mark attendance
            # markAttendance(name)
            #with app.app_context():
            mark_attendance(name)

        # Encode frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield buffer.tobytes()

    stop_camera()

def stop_camera():
    """Stop the camera feed"""
    global cap, running
    if cap:
        cap.release()
        cv2.destroyAllWindows()
        running = False
        print("Camera stopped.")
