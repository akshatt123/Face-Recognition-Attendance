import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from database import db
from models import Attendance
from app import db, app


def load_known_faces(folder='face_encodings'):
    """Load known face encodings and names from images in a folder."""
    known_faces = []
    known_names = []

    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return known_faces, known_names

    for file in os.listdir(folder):
        # Handle case-insensitive file extensions
        filename_lower = file.lower()
        if filename_lower.endswith((".jpg", ".png")):
            img_path = os.path.join(folder, file)
            img = cv2.imread(img_path)

            if img is not None:
                # Convert image to RGB format (required by face_recognition)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Detect face locations
                face_locations = face_recognition.face_locations(img_rgb)
                if not face_locations:
                    print(f"No faces detected in {file}. Skipping...")
                    continue
                
                # Generate face encodings
                encodings = face_recognition.face_encodings(img_rgb, face_locations)
                
                # Use the first detected face in the image
                if encodings:
                    known_faces.append(encodings[0])
                    known_names.append(os.path.splitext(file)[0])
                    print(f"Successfully processed {file}")
                else:
                    print(f"Could not generate encoding for {file}")
            else:
                print(f"Failed to load image {file}")


            

    print(f"Loaded {len(known_faces)} known faces.")
    return known_faces, known_names


#---------------------------------------------------------------------------------------


# ##this function was used to store the attendance record only in attendance.csv file
# def markAttendance(name, filename='attendance.csv'):
#     """Marks attendance only once per script execution."""

#     # Create CSV file if it doesn't exist
#     if not os.path.exists(filename):
#         with open(filename, 'w') as f:
#             f.write("SessionID,Name,Time\n")

#     # Read existing records
#     recorded_sessions = set()
#     with open(filename, 'r') as f:
#         for line in f.readlines():
#             data = line.strip().split(',')
#             if len(data) >= 2:
#                 recorded_sessions.add((data[0], data[1]))  # (SessionID, Name)

#     # Mark attendance only if name is not recorded in this session
#     if (SESSION_ID, name) not in recorded_sessions:
#         now = datetime.now().strftime('%H:%M:%S')
#         with open(filename, 'a') as f:
#             f.write(f'{SESSION_ID},{name},{now}\n')
#         print(f"✅ Marked attendance for {name} at {now}.")

#------------------------------------------------------------------------


#this function was recording and marking attendace within microseconds of camera openng and
#  was not able to send msg to user taht his attendance is marked

# def get_session_id():
#     """Generate a unique session ID based on script start time."""
#     return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# # Generate a unique session ID at script start (DO NOT regenerate inside function)
# SESSION_ID = get_session_id()


# def mark_attendance(name,filename='attendance.csv'):
#     """Mark attendance in the database if not already recorded."""
#     recorded_attendance = set()

#     # Mark attendance only if name is not recorded in this session
#     if (SESSION_ID, name) not in recorded_attendance:
#         now = datetime.now().strftime('%H:%M:%S')
#         with open(filename, 'a') as f:
#             f.write(f'{SESSION_ID},{name},{now}\n')
#         print(f"✅ Marked attendance for {name} at {now}.")

#     recorded_attendance.add(name)
#     new_entry = Attendance(name=name, timestamp=datetime.now())
#     db.session.add(new_entry)
#     db.session.commit()
#     return True 

##--------------------------------------------------------------------






# Temporary session file (cleared every run)
SESSION_FILE = ".session_log"

def get_session_id():
    """Generate a unique session ID based on script start time."""
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# ✅ Generate session ID at script start (DO NOT regenerate inside function)
SESSION_ID = get_session_id()

# Ensure session file exists
if not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "w") as f:
        f.write("")  # Create an empty file

# Global variable for frontend updates
latest_attendance_message = ""

def mark_attendance(name, filename='attendance.csv'):
    """Mark attendance if not already recorded in this session."""
    global latest_attendance_message  

    if name == "Unknown":
        return  # Ignore unknown faces

    # Read session file to track attendance
    with open(SESSION_FILE, "r") as f:
        recorded_attendance = set(f.read().splitlines())

    # Check if attendance already recorded in this session
    if name in recorded_attendance:
        latest_attendance_message = f"⏳ Attendance for {name} already recorded in this session."
        print(latest_attendance_message) 
        return  

    try:
        # Mark attendance time
        now = datetime.now().strftime('%H:%M:%S')

        # Append to CSV file for ease of getting attendance history
        with open(filename, 'a') as f:
            f.write(f'{SESSION_ID},{name},{now}\n')

        # Updating in attendance in database
        with app.app_context():  
            attendance_record = Attendance(name=name, timestamp=datetime.now())
            db.session.add(attendance_record)
            db.session.commit()

        # Update session file
        with open(SESSION_FILE, "a") as f:
            f.write(name + "\n")

        # Print success message
        latest_attendance_message = f"✔ Marked attendance for {name} at {now}."
        print(latest_attendance_message) 

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        latest_attendance_message = f"❌ Error marking attendance: {e}"
        print(latest_attendance_message)















