from flask import Flask, jsonify, render_template, Response
import threading
import main
from database import db
from models import Attendance
from datetime import datetime
from threading import Lock

app = Flask(__name__, 
            static_folder="../frontend/static", 
            template_folder="../frontend/templates")

app.config.from_object("config.Config")  # Load database config
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    """Generate frames from main.py"""
    try:
        for frame in main.start_camera():
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        print("Video streaming stopped")

@app.route('/video_feed')
def video_feed():
    """Returns the video stream"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


latest_attendance_message = ""  # Global variable to store the latest message

@app.route('/start_camera', methods=['GET'])
def start_camera():
    """Start the face recognition stream and reset latest message."""
    global latest_attendance_message
    latest_attendance_message = "Waiting for attendance capture..."
    
    threading.Thread(target=main.start_camera, daemon=True).start()
    
    return jsonify({
        "message": "Camera started",
        "latest_attendance": latest_attendance_message
    }), 200

@app.route('/latest_attendance_message', methods=['GET'])
def get_latest_attendance_message():
    """Send the latest attendance message to frontend"""
    return jsonify({"message": latest_attendance_message})


@app.route('/attendance_records', methods=['GET'])
def attendance_records():
    """Fetch latest attendance records"""
    records = Attendance.query.order_by(Attendance.timestamp.desc()).limit(10).all()
    return jsonify([{"name": rec.name, "timestamp": rec.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for rec in records])



@app.route('/stop_camera', methods=['GET'])
def stop_camera():
    """Stop the camera."""
    main.stop_camera()
    return jsonify({"message": "Camera stopped"}), 200

# Global session management
SESSION_ID = datetime.now().strftime('%Y%m%d%H%M%S')
recorded_names = set()
session_lock = Lock()




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist before running
    app.run(host='0.0.0.0', port=5000, debug=True)




