from database import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    session_id = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Attendance {self.name} at {self.timestamp}>"
