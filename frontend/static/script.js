let lastFrameTime = Date.now();
let checkingAttendance = false; // Avoid multiple API calls

document.getElementById("start-camera").addEventListener("click", function() {
    fetch("/start_camera")
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById("video-feed").src = "/video_feed";
            document.getElementById("video-feed").style.display = "block";
            document.getElementById("stop-camera").disabled = false;
            this.disabled = true;
            monitorFrameUpdates(); // Start monitoring for freeze
           listenForAttendanceUpdate(); // Start listening for updates
        })
        .catch(error => console.error("Error starting camera:", error));
});

document.getElementById("stop-camera").addEventListener("click", function() {
    fetch("/stop_camera")
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById("video-feed").src = "";
            document.getElementById("video-feed").style.display = "none";
            document.getElementById("start-camera").disabled = false;
            this.disabled = true;
            document.getElementById("attendance-message").innerHTML = "Camera stopped.";
        })
        .catch(error => console.error("Error stopping camera:", error));
});



// Function to monitor camera frame updates
function monitorFrameUpdates() {
    setInterval(() => {
        let currentTime = Date.now();
        let videoFeed = document.getElementById("video-feed");

        if (videoFeed && videoFeed.src) {
            if (currentTime - lastFrameTime > 1000) {  // If the frame hasn't updated in over 1s
                if (!checkingAttendance) {
                    checkingAttendance = true;
                    console.log("⚠ Camera frozen detected! Fetching latest attendance...");
                    fetchAttendance();
                }
            } else {
                checkingAttendance = false;  // Reset flag when frames are updating normally
            }
        }
    }, 1000);
}

// Function to fetch the latest attendance record
function fetchAttendance() { 
    fetch('/latest_attendance_message')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("📢 Fetched Attendance:", data);

            let messageElement = document.getElementById("attendance-message");

            if (data.name && data.timestamp) {
                let attendanceMessage = `✔ Attendance recorded for <b>${data.name}</b> at ${data.timestamp}`;
                showMessage(attendanceMessage, "green");
                messageElement.innerHTML = attendanceMessage;
            } else {
                let noAttendanceMessage = "ℹ No attendance recorded yet.";
                showMessage(noAttendanceMessage, "gray");
                messageElement.innerHTML = noAttendanceMessage;
            }
        })
        .catch(error => {
            console.error("❌ Error fetching attendance:", error);
            showMessage("⚠ Failed to fetch attendance. Please try again.", "red");
        });
}


// Listen for attendance updates using polling
function listenForAttendanceUpdate() {
    setInterval(() => {
        fetch('/latest_attendance_message')
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log("Received Attendance Update:", data.message);
                    showMessage(data.message, "green");
                }
            })
            .catch(error => console.error("Error fetching live attendance message:", error));
    }, 1500); // Polling every 1.5 seconds
}

// Utility function to show messages
function showMessage(message, color) {
    let messageBox = document.getElementById("attendance-message");
    messageBox.innerHTML = message;
    messageBox.style.color = color;
}
